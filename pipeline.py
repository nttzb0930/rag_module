
from rag_module.retrieval import retrieve_documents
import time

def rag_pipeline(
    question: str,
    sub_questions,
    chapter_number,
    vectorstore,
    combined_docs,
    embed_model,
    llm,
    bm25_cache_path=None,
):
    """
    
    """
    # # (1) rag_module/routing/pipeline
    # t0 = time.perf_counter()
    # chapter_number, sub_questions = route_and_split(
    #     question=question,
    #     chapter_titles=chapter_titles,
    # )

    # (2) rag_module/retrieval/pipeline
    t0= time.perf_counter()
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
    t1 = time.perf_counter()
    answer = llm.answer(
        question=question,
        docs=docs,
    )
    t2 = time.perf_counter()
    # print(f"[TIME] Routing: {t1 - t0:.2f}s")
    print(f"[TIME] Retrieval: {t1 - t0:.2f}s")
    print(f"[TIME] Generation: {t2 - t1:.2f}s")
    return answer

def summary_pipeline(
    question: str,
    sub_questions,
    chapter_number,
    vectorstore,
    combined_docs,
    embed_model,
    llm,
    bm25_cache_path=None,
):
    """

    """
    # # (1) rag_module/routing/pipeline
    # t0 = time.perf_counter()
    # chapter_number, sub_questions = route_and_split(
    #     question=question,
    #     chapter_titles=chapter_titles,
    # )
    
    # (2) rag_module/retrieval/pipeline
    t0 = time.perf_counter()
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
    t1 = time.perf_counter()
    answer = llm.summarize(
        question=question,###
        docs=docs,
    )
    t2 = time.perf_counter()
    # print(f"[TIME] Routing: {t1 - t0:.2f}s")
    print(f"[TIME] Retrieval: {t1 - t0:.2f}s")
    print(f"[TIME] Generation: {t2 - t1:.2f}s")
    return answer

