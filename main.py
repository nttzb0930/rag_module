from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_module.routing import (
    route_and_split, 
    parse_corpus_response,
    route_doc,
    intent_route,
)
from rag_module.vectorstore import (
    load_or_build_lsd_vectorstore,
    load_or_build_ktct_vectorstore,
    load_or_build_triet_vectorstore,
    RedisAnswerStore,
    PineconeEmbCache,
)
from rag_module.ingestion import (
    load_or_build_lsd,
    load_or_build_ktct,
    load_or_build_triet,
)
from rag_module.pipeline import (
    rag_pipeline,
    summary_pipeline,
)
from rag_module.config import (
    EMBED_MODEL,
    BM25_CACHE_PATH_LSD,
    BM25_CACHE_PATH_KTCT,
    BM25_CACHE_PATH_TRIET,
    PINECONE_INDEX,
    CORS_ALLOWED_ORIGINS,
    CORS_ALLOW_ORIGIN_REGEX,
)
from rag_module.generation import get_generation_service
from rag_module.prompts import ROUTE_CORPUS_PROMPT
from rag_module.utils import extract_answers_from_output, build_final_answer
import os

# Global state
semantic_cache = None
redis_store = None
llm = None
lsd_combined_docs = None
lsd_chapter_titles = None
lsd_vectorstore = None

ktct_combined_docs = None
ktct_chapter_titles = None
ktct_vectorstore = None

triet_combined_docs = None
triet_chapter_titles = None
triet_vectorstore = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pinecone_emb_ans, redis_store_ans
    global llm 
    global lsd_combined_docs, lsd_chapter_titles, lsd_vectorstore
    global ktct_combined_docs, ktct_chapter_titles, ktct_vectorstore
    global triet_combined_docs, triet_chapter_titles, triet_vectorstore
    # redis_store chia theo từng môn học rồi loafd từ đó tương tự với pinecone
    redis_store_ans = RedisAnswerStore(redis_url=os.getenv("REDIS_URL"), prefix="lsd:")
    pinecone_emb_ans = PineconeEmbCache(
        index_name=PINECONE_INDEX, # rename lsdembcache
        embed_model=EMBED_MODEL,
        redis_store=redis_store_ans,
    )
    llm = get_generation_service()
    # 1) Load/build corpus (từ cache .pkl)
    lsd_combined_docs, lsd_chapter_titles = load_or_build_lsd()
    ktct_combined_docs, ktct_chapter_titles = load_or_build_ktct()
    triet_combined_docs, triet_chapter_titles = load_or_build_triet()
    # 2) Load/build vectorstore
    lsd_vectorstore = load_or_build_lsd_vectorstore()
    ktct_vectorstore = load_or_build_ktct_vectorstore()
    triet_vectorstore = load_or_build_triet_vectorstore()

    print(f"[API] Startup Done: Corpus & Vectorstore Loaded")
    yield

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

def select_corpus(question: str):
    corpus = route_doc(question)
    if corpus is None:
        prompt = ROUTE_CORPUS_PROMPT.format(question=question)
        try:
            raw= llm.generate(prompt)
            corpus = parse_corpus_response(raw)
        except Exception:
            return (None, None, None, None)
    if corpus == "ktct":
        return (
            corpus,
            ktct_chapter_titles,
            ktct_combined_docs,
            ktct_vectorstore,
            BM25_CACHE_PATH_KTCT
        )
    elif corpus == 'triet':
        return (
            corpus,
            triet_chapter_titles,
            triet_combined_docs,
            triet_vectorstore,
            BM25_CACHE_PATH_TRIET,
        )
    elif corpus == 'lsd':
        return (
            corpus,
            lsd_chapter_titles,
            lsd_combined_docs,
            lsd_vectorstore,
            BM25_CACHE_PATH_LSD,
        )
    else:
        return (corpus, None, None, None, None) # handle corpus: unknown
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_origin_regex=CORS_ALLOW_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/rag", response_model=QueryResponse)
def rag_endpoint(payload: QueryRequest):
    question = payload.question
    pre_corpus = route_doc(question)
    if pre_corpus in ("lsd", "ktct", "triet"):
        cached_answer, _ = pinecone_emb_ans.check_cache_pinecone(
            question,
            [],
            scope=pre_corpus,
        )
        if isinstance(cached_answer, str):
            return QueryResponse(answer=cached_answer)

    # IntentRouter
    print("-"*100)
    raw_intent = intent_route(question, llm)
    print(f'[DEBUG] Intent Route: {raw_intent}')
    """
    {'handled': False, 'intent': 'unknown', 'confidence': 0.0}  -> Gọi LLM Xử Lý
    {'ask': 'Chủ trương của Đảng nhằm bảo vệ và giữ vững chính quyền cách mạng (9/1945–12/1946) là gì?', 'handled': True, 'intent': 'study', 'need_more_information': False, 'needs_normalization': False, 'normalized_query': 'Chủ trương của Đảng nhằm bảo vệ và giữ vững chính quyền cách mạng (9/1945–12/1946) là 
    gì?', 'sub_questions': []}
    """
    intent = raw_intent['intent']
    if not raw_intent['handled']:
        return QueryResponse(answer=raw_intent.get("message", "Vui lòng cung cấp thêm thông tin."))
    if intent in ("chitchat", "general_qa"):
        return QueryResponse(answer=raw_intent.get("answer", ""))
    query = raw_intent.get("normalized_query") or raw_intent.get("ask") or question
    corpus, chapter_titles, combined_docs, vectorstore, bm25_cache_path = select_corpus(question)
    if corpus == 'unknown':
        return QueryResponse(answer="Xin lỗi, không thể xác định được chủ đề câu hỏi. Vui lòng hỏi lại với câu hỏi rõ ràng hơn.")
    if not chapter_titles:
        raise ValueError("Chapter Titles Not Null!")

    cached_answer, _ = pinecone_emb_ans.check_cache_pinecone(
        query,
        [],
        scope=corpus,
    )
    if isinstance(cached_answer, str):
        return QueryResponse(answer=cached_answer)
    
    # dựa vào chapter titles cung cấp cho prompt xác định chapter number and sub question
    chapter_number, sub_questions = route_and_split(query, chapter_titles, llm)

    # Cache Questions
    cached_answers, sq_need_retrieval = pinecone_emb_ans.check_cache_pinecone(
        query, 
        sub_questions,
        scope=corpus
    )
    # Câu Đơn
    if isinstance(cached_answers, str):
        return QueryResponse(answer=cached_answers)
    # Câu Có Sub Question
    elif isinstance(cached_answers, dict) and not sq_need_retrieval:
        final_answer = build_final_answer(sub_questions, cached_answers)
        return QueryResponse(answer=final_answer)
    final_map = dict(cached_answers) if cached_answers else {}

    # 
    if sq_need_retrieval and intent == "study":
        print(f"[DEBUG] Starting retrieval for {len(sq_need_retrieval)} sub questions...")
        answer = rag_pipeline(
            question=query,
            sub_questions=sq_need_retrieval,
            chapter_number=chapter_number,
            vectorstore=vectorstore,
            combined_docs=combined_docs,
            embed_model=EMBED_MODEL,
            bm25_cache_path=bm25_cache_path,
            llm=llm,
        )
        
        # Parse tất cả answers từ LLM output
        parsed_answers = extract_answers_from_output(answer, len(sq_need_retrieval)) # {}
        print(f"[DEBUG] Parsed answers: {list(parsed_answers.keys())}")

        
        # Update final_map và cache cho từng sub_question
        for i, sq in enumerate(sq_need_retrieval, start=1):
            if i in parsed_answers:
                sq_ans = parsed_answers[i]
                final_map[sq] = sq_ans
                pinecone_emb_ans.set(sq, sq_ans, scope=corpus)
                print(f"[DEBUG] Cached new answer for: {sq}")
            else:
                print(f"[WARN] Không parse được answer cho sub question: {sq}")
    # Build final answer từ final_map
    final_answer = build_final_answer(sub_questions or sq_need_retrieval, final_map)
    return QueryResponse(answer=final_answer)



        



    
