def deduplicate_docs(docs, type_name: str):
    before = len(docs)
    unique = {}
    for d in docs:
        key = (
            d.page_content,
            d.metadata.get("number"),
            d.metadata.get("chapter_number")
        )
        unique[key] = d
    deduped = list(unique.values())
    after = len(deduped)
    print(f"[DEBUG] Dedup {type_name}: Docs Before: {before} -> Docs After: {after} (Removed {before - after} Duplicates)")
    return deduped
