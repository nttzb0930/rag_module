import pickle
import os
from rank_bm25 import BM25Okapi
import numpy as np


def load_or_build_bm25(combined_docs, cache_path: str | None = None):
    """
    Build hoặc load BM25 index theo từng chapter.

    - Nếu `cache_path` được truyền và file tồn tại -> load từ cache.
    - Nếu `cache_path` được truyền nhưng chưa có file -> build rồi lưu.
    - Nếu `cache_path` là None -> luôn build mới (không cache).
    """
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            bm25_by_chapter = pickle.load(f)
    else:
        bm25_by_chapter = build_bm25_by_chapter(combined_docs)
        if cache_path:
            with open(cache_path, "wb") as f:
                pickle.dump(bm25_by_chapter, f)
    return bm25_by_chapter

def build_bm25_by_chapter(combined_docs):
    """
    Build BM25 index theo từng chapter
    Chỉ build 1 lần
    """
    bm25_by_chapter = {}

    for ch in set(d.metadata["chapter_number"] for d in combined_docs):
        docs_ch = [
            d for d in combined_docs
            if d.metadata["chapter_number"] == ch
        ]

        corpus = [d.page_content for d in docs_ch]

        tokenized = [c.split() for c in corpus]

        bm25_by_chapter[ch] = {
            "bm25": BM25Okapi(tokenized),
            "docs": docs_ch
        }

    return bm25_by_chapter




def bm25_search_by_chapter(
    bm25_by_chapter,
    chapter_number,
    questions,
    top_k
):
    """
    BM25 search trong 1 chương
    """
    pack = bm25_by_chapter.get(chapter_number)
    if not pack:
        return []

    bm25 = pack["bm25"]
    docs = pack["docs"]

    results = []

    for q in questions:
        scores = bm25.get_scores(q.split())
        top_idx = np.argsort(scores)[::-1][:top_k]

        results.extend(docs[i] for i in top_idx)

    return results
