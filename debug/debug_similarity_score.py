def debug_similarity_search_with_score(semantic_docs, semantic_scores):
    # ========================== DEBUG SIMILARITY SCORE ==================
    # return distance giữa embedding với câu hỏi và docs -> càng gần 0 càng match 
    print(f"-------------------- SIMILARITY SEARCH WITH SCORE --------------------")
    for d, s in zip(semantic_docs, semantic_scores):
        meta = d.metadata or {}
        title = meta.get("title") or meta.get("chapter_title") or ""
        print(f"[SIM] Semantic Score = {s:.4f} - Title = {title!r}\n"
            f"Content Start: {d.page_content[:100]}\nContent End: {d.page_content[-100:]}\n"
            f"{'-'*100}")
    # ============================ END DEBUG =============================