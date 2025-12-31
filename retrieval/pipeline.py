from .semantic import semantic_retrieve_with_scores
from .bm25 import load_or_build_bm25, bm25_search_by_chapter
from .dedup import deduplicate_docs
from .hybrid import hybrid_mmr_retrieve
from rag_module.debug import debug_similarity_search_with_score, debug_final_docs_ok




def retrieve_documents(
    question,
    sub_questions,
    chapter_number,
    vectorstore,
    combined_docs,
    embed_model,
    bm25_cache_path=None,
):
    """
    1. Semantic Search Với Từng Sub Question Và Chương Đó
    2. BM25 Trên Chương Đó  Search Tìm Ra Top 5 
    3. Lọc Trùng
    4. Final Docs Cuối Cùng Ném Vào Prompt Làm Context
    """
    def expand(final_doc, combined_docs):
        # Mở rộng khi gặp bullet 
        expanded_docs = [final_doc]

        meta = getattr(final_doc, "metadata", {}) or {}
        if meta.get("type") != "bullet":
            return expanded_docs

        number = meta.get("number")
        bullet_index = meta.get("bullet_index")

        # Kéo thêm các bullet cùng cấp
        for other in combined_docs:
            m2 = getattr(other, "metadata", {}) or {}
            if (
                m2.get("type") == "bullet"
                and m2.get("number") == number
                and m2.get("bullet_index") != bullet_index
                and other not in expanded_docs
            ):
                expanded_docs.append(other)

        return expanded_docs
    # Semantic Search From VectorStore (Default Call)
    semantic_docs, semantic_scores = semantic_retrieve_with_scores(
        vectorstore,
        sub_questions,
        chapter_number,
        k=3
    )

    final_docs = []
    # Test với câu hỏi đơn thì chỉ dùng semantic search hoặc bm25 top 1 làm context (cần split chuẩn)
    if len(sub_questions) <= 1:
        if semantic_docs:
            debug_similarity_search_with_score(semantic_docs, semantic_scores)
            best_score = min(semantic_scores)
            best_idx = semantic_scores.index(best_score)
            best_doc = semantic_docs[best_idx]
            meta = getattr(best_doc, "metadata", {}) or {}
            if best_score <= 0.5:
                # chỉ lấy ra best docs với score
                # test kéo thêm nếu doc là bullet và kéo thêm bullet cùng cấp
                #final_docs.append(semantic_docs[best_idx])
                print(f"Tìm thấy best_doc với score {best_score} -> Thử mở rộng")
                if meta.get('type') == "bullet":
                    final_docs = expand(semantic_docs[best_idx], combined_docs)
                    print(f'Tìm thấy {len(final_docs)} liên kết best_doc')
                else:
                    final_docs = [best_doc]
                    print("Không tìm thấy docs match với best_doc")
            else:
                # dùng full semantic_docs ban đầu
                final_docs = semantic_docs
        else:
            print(f"[DEBUG] semantic_docs trống")

    else:
        bm25_map = load_or_build_bm25(combined_docs, cache_path=bm25_cache_path)
        bm25_docs = bm25_search_by_chapter(bm25_map, chapter_number, sub_questions, top_k=3)
        semantic_docs = deduplicate_docs(semantic_docs, type_name="Similarity_Search")
        bm25_docs = deduplicate_docs(bm25_docs, type_name="BM25_Search")
        unique_docs = deduplicate_docs(semantic_docs + bm25_docs, type_name="Unique")
        final_docs = hybrid_mmr_retrieve(
            question,
            unique_docs,
            embed_model,
            bm25_k=3,
            mmr_k=3,
            )
        print(
            f"[DEBUG] Retrieval: Semantic: {len(semantic_docs)} & "
            f"BM25: {len(bm25_docs)} -> Unique: {len(unique_docs)} -> Final: {len(final_docs)}"
        )
    debug_final_docs_ok(final_docs)
    return final_docs
