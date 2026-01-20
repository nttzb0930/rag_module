import os
import time
import uuid
import numpy as np
from typing import Optional
from pinecone.grpc import PineconeGRPC as Pinecone

class PineconeEmbCache:
    """
    Semantic Cache:
    - Pinecone: vector search -> returns best_id + score
    - RedisAnswerStore: stores payload/answer by id with TTL
    """

    def __init__(
        self,
        index_name: str,
        embed_model,
        redis_store,           
        threshold: float = 0.9,
        topk: int = 5,
    ):
        self.embed_model = embed_model
        self.redis_store = redis_store
        self.threshold = threshold
        self.topk = topk
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY is missing")

        pc = Pinecone(api_key=api_key)
        self.index = pc.Index(index_name)

    @staticmethod
    def _normalize(v: np.ndarray) -> np.ndarray:
        v = v.astype(np.float32)
        return v / (np.linalg.norm(v) + 1e-9)

    def _embed(self, text: str) -> list[float]:
        vec = self.embed_model.encode([text])[0]
        vec = self._normalize(np.asarray(vec, dtype=np.float32))
        return vec.tolist()

    def get(self, question: str, scope: str) -> Optional[str]:
        """
        1) query Pinecone
        2) nếu best_score >= threshold -> RedisAnswerStore.get_answer(best_id)
        """
        
        try:
            qvec = self._embed(question)
            res = self.index.query(
                vector=qvec,
                top_k=self.topk,
                filter={"scope": {"$eq": scope}},
            )
        except Exception as e:
            print("[PINECONE QUERY ERROR]", repr(e))
            return None
        """ $res
        QueryResponse(
            matches=[
                {
                id='fc2888916e7f4bbbab748afb5914ffe5',
                score=0.8906097412109375,
                metadata=None,
                sparse_values=None,
                values=[]
                },
                {
                id='4e2d1b5f5f5b49b89f0999ac86ceca71',
                score=0.5321750640869141,
                metadata=None,
                sparse_values=None,
                values=[]
                }
            ],
            namespace='',
            usage={'read_units': 1},
            _response_info={
                'raw_headers': {
                'date': 'Wed, 14 Jan 2026 15:12:05 GMT',
                'x-pinecone-max-indexed-lsn': '6',
                'x-pinecone-request-latency-ms': '96',
                'x-pinecone-request-id': '664098688639106927',
                'x-envoy-upstream-service-time': '113',
                'x-pinecone-response-duration-ms': '114',
                'server': 'envoy'
                }
            }
        )
        """
        matches = getattr(res, "matches", None) or []
        if not matches:
            return None
        best_doc = matches[0]
        best_id = str(best_doc.id)
        best_score = float(best_doc.score)
        if best_score < self.threshold:
            return None
        # tam thoi khong co ttl xu ly delete sau 24h hoac khi ket thuc phien chat sau...
        return self.redis_store.get_answer(best_id)
        

    def set(self, question: str, answer: str, scope: str) -> str:
        """
        1) create id
        2) Redis set lsd:{id}
        3) Pinecone upsert (id, vector)
        """
        _id = uuid.uuid4().hex
        now = int(time.time())
        ok = self.redis_store.set_payload(
            _id,
            {
                "question": question, 
                "answer": answer, 
                "created_at": now,
            },
        )
        if not ok:
            return ""

        try:
            vec = self._embed(question)
            self.index.upsert(
                vectors=[(
                _id,
                vec, 
                {
                    "created_at": now,
                    "scope": scope,
                }     
            )]
            )
        except Exception as e:
            print("[PINECONE UPSERT ERROR]", repr(e))
            # Redis đã có answer nhưng Pinecone không có vector -> cache này không semantic-search được
            return _id

        return _id
    def check_cache_pinecone(self, question: str, sub_questions: list[str], scope: str):
        """
        Cache Theo Từng Sub Question
        Nếu Câu Đơn Thì Return
        Nếu Câu Có Sub Question Thì Cache Theo Từng Sub Question
        Trường Hợp Sub Question Đó Chưa Có Trong Cache Thì Append Vào sq_need_retrieval Để Retrieval Rồi Mới Đưa Vào Cache
        """
        cached_answers = {}
        sq_need_retrieval = []
  
        # Check Cache

        # Câu đôi
        if sub_questions and len(sub_questions) > 1:
            # Nhiều sub_questions nếu cache thì append vào cached_answers chính là answer lưu trong redis
            for sq in sub_questions:
                answer = self.get(sq, scope)
                if answer:
                    print(f"[CACHE HIT] {sq}")
                    cached_answers[sq] = answer
                else:
                    sq_need_retrieval.append(sq)
            # Nếu tất cả cache hit → return
            if not sq_need_retrieval:
                # ADD FORMAT QUESTION: ANSWER IN HERE
                """
                    1. Câu hỏi
                    - Câu trả lời
                """
                final_answer = "\n\n".join(
                    f"{i+1}. {sq}\n- {cached_answers[sq]}"
                    for i, sq in enumerate(sub_questions)
                )
                return final_answer, []
            return cached_answers, sq_need_retrieval
        # Câu đơn hoặc subquestions = []
        check_question =  [0] if sub_questions else question
        result = self.get(check_question, scope)
        if result:
            return result, []    
        sq_need_retrieval = sub_questions if sub_questions else [question]
        return None, sq_need_retrieval
    