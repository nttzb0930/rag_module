def debug_ranking_docs_ok(
    top_docs, topk_idx, bm25_scores, cos_scores, hybrid_scores, selected
):
    print("\n========== DEBUG RANKING (WITH DOC INFO) ==========\n")

    # Helper: rút gọn nội dung
    def short(text, n=80):
        text = text.replace("\n", " ")
        return text[:n] + ("..." if len(text) > n else "")

    # ---- BM25 ----
    print("🔍 BM25 Ranking (local → global):")
    for i, score in sorted(enumerate(bm25_scores), key=lambda x: -x[1]):
        doc = top_docs[i]
        print(
            f"\n  Local {i} (Global {topk_idx[i]}) | BM25={score:.4f}\n"
            f"    → type: {doc.metadata.get('type')}\n"
            f"    → number: {doc.metadata.get('number')}\n"
            f"    → title: {doc.metadata.get('title')}\n"
            f"    → content: {short(doc.page_content)}"
        )

    print("\n\n🔍 Cosine Similarity Ranking:")
    for i, score in sorted(enumerate(cos_scores), key=lambda x: -x[1]):
        doc = top_docs[i]
        print(
            f"\n  Local {i} (Global {topk_idx[i]}) | CosSim={score:.4f}\n"
            f"    → type: {doc.metadata.get('type')}\n"
            f"    → number: {doc.metadata.get('number')}\n"
            f"    → title: {doc.metadata.get('title')}\n"
            f"    → content: {short(doc.page_content)}"
        )

    print("\n\n🔍 Hybrid Score Ranking:")
    for i, score in sorted(enumerate(hybrid_scores), key=lambda x: -x[1]):
        doc = top_docs[i]
        print(
            f"\n  Local {i} (Global {topk_idx[i]}) | Hybrid={score:.4f}\n"
            f"    (Cos={cos_scores[i]:.4f}, BM25={bm25_scores[i]:.4f})\n"
            f"    → type: {doc.metadata.get('type')}\n"
            f"    → number: {doc.metadata.get('number')}\n"
            f"    → title: {doc.metadata.get('title')}\n"
            f"    → content: {short(doc.page_content)}"
        )

    # ---- MMR ----
    print("\n\n🏆 MMR Selected Docs:")
    for step, local_idx in enumerate(selected, start=1):
        doc = top_docs[local_idx]
        print(
            f"\n  Step {step}: Local {local_idx} (Global {topk_idx[local_idx]})\n"
            f"    → type: {doc.metadata.get('type')}\n"
            f"    → number: {doc.metadata.get('number')}\n"
            f"    → title: {doc.metadata.get('title')}\n"
            f"    → content: {short(doc.page_content)}"
        )

    print("\n===================================\n")
# debug_ranking_docs(
#     top_docs=bm25_top_docs,         # hoặc top_docs trong hybrid pipeline
#     topk_idx=debug_info["bm25_idx"],
#     bm25_scores=debug_info["bm25_scores"],
#     cos_scores=debug_info["cos_scores"],
#     hybrid_scores=debug_info["hybrid_scores"],
#     selected=debug_info["selected_local"]
# )
