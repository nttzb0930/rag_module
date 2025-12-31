from rank_bm25 import BM25Okapi
import numpy as np

def bm25_rerank(query, docs, top_k=5):
    corpus = [d.page_content for d in docs]
    tokenized = [c.split() for c in corpus]

    bm25 = BM25Okapi(tokenized)
    scores = bm25.get_scores(query.split())

    top_idx = np.argsort(scores)[::-1][:top_k]
    return [docs[i] for i in top_idx]
