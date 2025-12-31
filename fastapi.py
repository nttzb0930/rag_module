from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from rag_module.semantic_router import semantic_router
from rag_module.generation import get_generation_service
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
    rag_pipeline_stream,
)
from rag_module.config import (
    EMBED_MODEL,
    BM25_CACHE_PATH_LSD,
    BM25_CACHE_PATH_KTCT,
    BM25_CACHE_PATH_TRIET,
)
from rag_module.routing.doc_router import route_doc


# cache câu hỏi câu trả lời nhưng user có thể thay đổi vài từ lên không cache đúng
# semantic embed question và question mới tính cosine similarity > 0.9 thì lấy ra còn không thì render từ vector ra


# Global state
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
    global lsd_combined_docs, lsd_chapter_titles, lsd_vectorstore
    global ktct_combined_docs, ktct_chapter_titles, ktct_vectorstore
    global triet_combined_docs, triet_chapter_titles, triet_vectorstore

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
    print(f"[DEBUG] Doc Router -> {corpus}")
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

    cached = get_answer_from_redis(question)
    if cached:
        return QueryResponse(answer=cached)

    # chọn corpus theo nội dung câu hỏi
    chapter_titles, combined_docs, vectorstore, bm25_cache_path = select_corpus(question)
    if chapter_titles is None:
        gen = get_generation_service()
        answer = gen.llm.generate(question)
        return QueryResponse(answer=answer)
    scores = semantic_router.guide(question)
    best_score, best_route = scores[0]
    THRESHOLD = 0.35

    if best_route == "summary" and best_score >= THRESHOLD:
        answer = summary_pipeline(
            question=question,
            chapter_titles=chapter_titles,
            vectorstore=vectorstore,
            combined_docs=combined_docs,
            embed_model=EMBED_MODEL,
            bm25_cache_path=bm25_cache_path
        )
        set_answer_to_redis(question, answer)
    else:
        answer = rag_pipeline(
            question=question,
            chapter_titles=chapter_titles,
            vectorstore=vectorstore,
            combined_docs=combined_docs,
            embed_model=EMBED_MODEL,
            bm25_cache_path=bm25_cache_path
        )
        set_answer_to_redis(question, answer)

    return QueryResponse(answer=answer)


@app.post("/rag-stream")
def rag_stream(payload: QueryRequest):
    question = payload.question

    chapter_titles, combined_docs, vectorstore, bm25_cache_path = select_corpus(question)

    scores = semantic_router.guide(question)
    best_score, best_route = scores[0]
    THRESHOLD = 0.35

    def token_stream():
        if best_route == "summary" and best_score >= THRESHOLD:
            answer = summary_pipeline(
                question=question,
                chapter_titles=chapter_titles,
                vectorstore=vectorstore,
                combined_docs=combined_docs,
                embed_model=EMBED_MODEL,
                bm25_cache_path=bm25_cache_path,
            )
            yield answer
        else:
            for chunk in rag_pipeline_stream(
                question=question,
                chapter_titles=chapter_titles,
                vectorstore=vectorstore,
                combined_docs=combined_docs,
                embed_model=EMBED_MODEL,
                bm25_cache_path=bm25_cache_path
            ):
                yield chunk

    return StreamingResponse(token_stream(), media_type="text/plain")


