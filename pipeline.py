from rag_module.routing import route_and_split
from rag_module.retrieval import retrieve_documents
from rag_module.generation import get_generation_service
import time

def rag_pipeline(
    question: str,
    chapter_titles: list[str],
    vectorstore,
    combined_docs,
    embed_model,
    bm25_cache_path=None,
):
    """
    
    """
    # (1) rag_module/routing/pipeline
    t0 = time.perf_counter()
    chapter_number, sub_questions = route_and_split(
        question=question,
        chapter_titles=chapter_titles,
    )

    # (2) rag_module/retrieval/pipeline
    t1 = time.perf_counter()
    docs = retrieve_documents(
        question=question,
        sub_questions=sub_questions,
        chapter_number=chapter_number,
        vectorstore=vectorstore,
        combined_docs=combined_docs,
        embed_model=embed_model,
        bm25_cache_path=bm25_cache_path,
    )

    # (3) rag_module/generation/generate
    t2 = time.perf_counter()
    gen = get_generation_service()
    answer = gen.answer(
        question=question,
        docs=docs,
    )
    t3 = time.perf_counter()
    print(f"[TIME] Routing: {t1 - t0:.2f}s")
    print(f"[TIME] Retrieval: {t2 - t1:.2f}s")
    print(f"[TIME] Generation: {t3 - t2:.2f}s")
    return answer

def summary_pipeline(
    question: str,
    chapter_titles: list[str],
    vectorstore,
    combined_docs,
    embed_model,
    bm25_cache_path=None,
):
    """

    """
    # (1) rag_module/routing/pipeline
    t0 = time.perf_counter()
    chapter_number, sub_questions = route_and_split(
        question=question,
        chapter_titles=chapter_titles,
    )
    
    # (2) rag_module/retrieval/pipeline
    t1 = time.perf_counter()
    docs = retrieve_documents(
        question=question,
        sub_questions=sub_questions,
        chapter_number=chapter_number,
        vectorstore=vectorstore,
        combined_docs=combined_docs,
        embed_model=embed_model,
        bm25_cache_path=bm25_cache_path,
    )

    # (3) rag_module/generation/generate
    t2 = time.perf_counter()
    gen = get_generation_service()
    answer = gen.summarize(
        question=question,###
        docs=docs,
    )
    t3 = time.perf_counter()
    print(f"[TIME] Routing: {t1 - t0:.2f}s")
    print(f"[TIME] Retrieval: {t2 - t1:.2f}s")
    print(f"[TIME] Generation: {t3 - t2:.2f}s")
    return answer

def rag_pipeline_stream(
    question: str,
    chapter_titles: list[str],
    vectorstore,
    combined_docs,
    embed_model,
    bm25_cache_path=None,
):
    chapter_number, sub_questions = route_and_split(question=question,chapter_titles=chapter_titles)
    docs = retrieve_documents(
        question=question,
        sub_questions=sub_questions,
        chapter_number=chapter_number,
        vectorstore=vectorstore,
        combined_docs=combined_docs,
        embed_model=embed_model,
        bm25_cache_path=bm25_cache_path,
    )
    gen = get_generation_service()
    # build prompt từ docs + question
    for chunk in gen.stream(question, docs):
        yield chunk
