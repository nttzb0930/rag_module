from .samples import INTENT_ROUTES, GENERIC_STUDY_PHRASES, ENTITY_HINTS
import re

class IntentRule:
    def __init__(self, threshold=0.70):
        self.threshold = threshold

    @staticmethod
    def normalize_vi(s: str) -> str:
        s = s.strip().lower()
        s = re.sub(r"\s+", " ", s)
        return s

    def score_intent(self, query: str) -> dict:
        q = self.normalize_vi(query)

        def count_hits(phrases):
            hits = 0
            for p in sorted(phrases, key=len, reverse=True):
                pattern = r"(?<!\w)" + re.escape(self.normalize_vi(p)) + r"(?!\w)"
                if re.search(pattern, q):
                    hits += 1
            return hits

        return {k: count_hits(v) for k, v in INTENT_ROUTES.items()}

    def base_detect_intent(self, query: str):
        q = self.normalize_vi(query)
        scores = self.score_intent(q)

        if scores.get("summary", 0) > 0:
            return {"intent": "summary", "confidence": min(1.0, 0.6 + 0.2 * scores["summary"])}

        if scores.get("chitchat", 0) > 0 and len(q.split()) <= 6:
            return {"intent": "chitchat", "confidence": 0.85}

        if scores.get("study", 0) > 0 and ("?" in q or len(q.split()) >= 4):
            return {"intent": "study", "confidence": min(1.0, 0.55 + 0.15 * scores["study"])}

        return {"intent": "unknown", "confidence": 0.0}

    def step0_intent(self, query: str):
        out = self.base_detect_intent(query)
        if out["intent"] != "unknown" and out["confidence"] >= self.threshold:
            return {"handled": True, **out}
        return {"handled": False, **out}

    def need_more_info_cheap(self, query: str) -> bool:
        q = self.normalize_vi(query)
        has_generic = any(p in q for p in GENERIC_STUDY_PHRASES)
        has_entity = any(e in q for e in ENTITY_HINTS) or "?" in q
        return has_generic and (not has_entity)