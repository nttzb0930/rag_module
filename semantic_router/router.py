import numpy as np
from rag_module.config import EMBED_MODEL



class SemanticRouter:
    def __init__(self, routes, embedding=EMBED_MODEL):
        self.routes = routes
        self.embedding = embedding
        self.routes_embedding = {}

        for route in self.routes:
            embs = self.embedding.embed_documents(route.samples)
            embs = np.array(embs)
            # chuẩn hoá từng vector
            embs = embs / np.linalg.norm(embs, axis=1, keepdims=True)
            self.routes_embedding[route.name] = embs

    def guide(self, query: str):
        q_emb = np.array(self.embedding.embed_query(query))
        q_emb = q_emb / np.linalg.norm(q_emb)
        scores = []

        for route in self.routes:
            embs = self.routes_embedding[route.name]
            # cosine với tất cả samples của route, lấy mean
            score = float(np.mean(embs @ q_emb))
            scores.append((score, route.name))

        scores.sort(reverse=True)
        return scores
