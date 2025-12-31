# rag_module/retrieval/hybrid.py
from rag_module.debug import debug_ranking_docs_ok
from sklearn.preprocessing import minmax_scale
from rank_bm25 import BM25Okapi
import numpy as np
import os
def hybrid_mmr_retrieve(
    question,
    docs,
    embed_model,
    bm25_k,
    mmr_k,
    lambda_mult=0.6,
    w1=0.7,
    w2=0.3
):
    corpus = [d.page_content for d in docs]
    tokenized = [c.split() for c in corpus]

    
    bm25 = BM25Okapi(tokenized)

    scores = bm25.get_scores(question.split())
    top_idx = np.argsort(scores)[::-1][:bm25_k]
    top_docs = [docs[i] for i in top_idx]

    bm25_norm = minmax_scale(np.array(scores)[top_idx])

    query_emb = embed_model.encode(question)
    doc_embs = embed_model.encode([d.page_content for d in top_docs])
    # cosine similarity
    cos_scores = np.dot(doc_embs, query_emb) / (
        np.linalg.norm(doc_embs, axis=1) * np.linalg.norm(query_emb)
    )

    hybrid_scores = w1 * cos_scores + w2 * bm25_norm

    def cosine(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    selected = [int(np.argmax(hybrid_scores))]

    for _ in range(1, mmr_k):
        remain = [i for i in range(len(top_docs)) if i not in selected]
        mmr_scores = {}
        for i in remain:
            diversity = np.mean([cosine(doc_embs[i], doc_embs[j]) for j in selected])
            mmr_scores[i] = lambda_mult * hybrid_scores[i] - (1 - lambda_mult) * diversity
        selected.append(max(mmr_scores, key=mmr_scores.get))
    if os.getenv("DEBUG_RANKING") == "1":
        debug_ranking_docs_ok(
            top_docs=top_docs,
            topk_idx=top_idx,
            bm25_scores=bm25_norm,      # hoặc scores[top_idx] nếu muốn raw
            cos_scores=cos_scores,
            hybrid_scores=hybrid_scores,
            selected=selected,
        )
    return [top_docs[i] for i in selected]
