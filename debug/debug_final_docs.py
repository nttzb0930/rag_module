def debug_final_docs_ok(final_docs):
    # Debug final_docs (def)
    print("-------------------- DEBUG FINAL DOCS --------------------")
    for i, d in enumerate(final_docs[:5], start=1):
        meta = getattr(d, "metadata", {}) or {}
        ch = meta.get("chapter_number")
        num = meta.get("number")
        doc_type = meta.get("type")
        title = meta.get("title") or meta.get("chapter_title") or ""
        bullet_idx = meta.get("bullet_index")

        if bullet_idx is not None:
            print(f'[DEBUG] Doc[{i}] chapter_number={ch} - number={num} - type={doc_type} - title={title} - bullet_index={bullet_idx}\n'
                  f'Content Start: {d.page_content[:100]}\nContent End: {d.page_content[-100:]}\nContent Length: {len(d.page_content)}\n'
                  f"{'-'*100}")
        else:
            print(f"[DEBUG] Doc[{i}] chapter_number={ch} - number={num} - type={doc_type} - title={title!r}\n"
                  f"Content Start: {d.page_content[:100]}\nContent End: {d.page_content[-100:]}\nContent Length: {len(d.page_content)}\n"
                  f"{'-'*100}")

    print(f"[DEBUG] Retrieval: Final: {len(final_docs)} Docs Đưa Vào Context")