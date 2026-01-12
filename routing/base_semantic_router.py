from rag_module.config import EMBED_MODEL
import numpy as np



class BaseSemanticRouter:
    def __init__(self, routes, embedding=EMBED_MODEL, reducer="max", threshold=0.4, margin=0.1):
        self.routes = routes # dict {name: [samples]}
        self.embedding = embedding
        self.reducer = reducer
        self.threshold = threshold
        self.margin = margin
        self.routes_embedding = {
            name: np.array(self.embedding.encode(samples))
            for name, samples in routes.items()
            if samples and any(s.strip() for s in samples)
        }
    def cosine(self, a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))
    def score(self, query):
        q_emb = self.embedding.encode([query])[0]
        best_route = None
        best_score = -1
        second_score = -1

        for name, embeds in self.routes_embedding.items():
            if len(embeds) == 0:
                continue
            sims = [self.cosine(q_emb, e) for e in embeds]
            score = max(sims) if self.reducer == "max" else float(np.mean(sims))

            if score > best_score:
                second_score = best_score
                best_score = score
                best_route = name
            elif score > second_score:
                second_score = score

        return best_route, best_score, second_score
    def route(self, question: str):
        best, best_score, second = self.score(question)
        if best_score < self.threshold or (best_score - second) < self.margin:
            return None
        return best
