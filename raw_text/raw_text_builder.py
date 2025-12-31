def build_raw_text(docs, page_start=None, page_end=None):
    # (1) Xóa bớt những docs không cần dùng đến
    if page_start is None and page_end is None:
        page_start = 0
        page_end = len(docs)
    elif page_start is None or page_end is None:
        raise ValueError("Cần truyền cả page_start và page_end hoặc bỏ cả hai")
    cut_docs = [d for d in docs if d.metadata["page"] >= page_start and d.metadata["page"] < page_end]
    # (2) Convert Docs To String
    full_text = " ".join(d.page_content for d in cut_docs if d.page_content)
    return full_text

    
