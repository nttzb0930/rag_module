from contextlib import asynccontextmanager
from fastapi import FastAPI
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
    set_answer_to_redis,
    get_answer_from_redis,
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
)
from rag_module.generation import get_generation_service
from rag_module.prompts import ROUTE_CORPUS_PROMPT



# Global state
semantic_redis = None
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
    global semantic_redis
    global llm 
    global lsd_combined_docs, lsd_chapter_titles, lsd_vectorstore
    global ktct_combined_docs, ktct_chapter_titles, ktct_vectorstore
    global triet_combined_docs, triet_chapter_titles, triet_vectorstore

    semantic_redis = BaseSemanticRouter
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
            ktct_chapter_titles,
            ktct_combined_docs,
            ktct_vectorstore,
            BM25_CACHE_PATH_KTCT
        )
    elif corpus == 'triet':
        return (
            triet_chapter_titles,
            triet_combined_docs,
            triet_vectorstore,
            BM25_CACHE_PATH_TRIET,
        )
    elif corpus == 'lsd':
        return (
            lsd_chapter_titles,
            lsd_combined_docs,
            lsd_vectorstore,
            BM25_CACHE_PATH_LSD,
        )
    else:
        return (None, None, None, None)
app = FastAPI(lifespan=lifespan)
@app.post("/rag", response_model=QueryResponse)
def rag_endpoint(payload: QueryRequest):
    question = payload.question
    # Load Cache Question From Redis
    # cache câu hỏi câu trả lời nhưng user có thể thay đổi vài từ lên không cache đúng
    # semantic embed question và question mới tính cosine similarity > 0.9 thì lấy ra còn không thì render từ vector ra
    cached = get_answer_from_redis(question)
    if cached:
        return QueryResponse(answer=cached)
    # IntentRouter
    print("-"*100)
    raw_intent = intent_route(question, llm)
    print(raw_intent)
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
    chapter_titles, combined_docs, vectorstore, bm25_cache_path = select_corpus(question)
    if not chapter_titles:
        raise ValueError("Chapter Titles Not Null!")
    chapter_number, sub_questions = route_and_split(question, chapter_titles, llm)

    if intent == 'summary':
        answer = summary_pipeline(
            question=question,
            sub_questions=sub_questions,
            chapter_number=chapter_number,
            vectorstore=vectorstore,
            combined_docs=combined_docs,
            embed_model=EMBED_MODEL,
            bm25_cache_path=bm25_cache_path
        )
        set_answer_to_redis(question, answer)
    else:
        answer = rag_pipeline(
            question=question,
            sub_questions=sub_questions,
            chapter_number=chapter_number,
            vectorstore=vectorstore,
            combined_docs=combined_docs,
            embed_model=EMBED_MODEL,
            bm25_cache_path=bm25_cache_path
        )
        set_answer_to_redis(question, answer)

    return QueryResponse(answer=answer)




