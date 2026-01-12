from .router import DocRouter
from .samples import DOC_ROUTES, QUES_LSD

def route_doc(question: str) -> str:
    """
    Router Chọn Corpus
    - 1. Router Theo Keyword
    - 2. Router Theo Semantic
    - 3. Router Fallback Call LLM
    """
    q = question.strip().lower()
    if any(k in q for k in DOC_ROUTES['ktct']):
        return "ktct"
    if any(k in q for k in DOC_ROUTES['lsd']):
        return "lsd"
    if any(k in q for k in DOC_ROUTES['triet']):
        return "triet"
    return DocRouter().route(question) # Semantic dùng question gốc
if __name__ == "__main__":
    fails = []
    for i, q in enumerate(QUES_LSD["lsd"], start=1):
        corpus = route_doc(q)
        print(f"[{i}] {corpus} | {q}")
        if corpus != "lsd":
            fails.append((i, q, corpus))
    print(f"\nOK: {len(QUES_LSD['lsd']) - len(fails)}, FAIL: {len(fails)}")
    if fails:
        for i, q, c in fails:
            print(f"  - Fail #{i}: {q} (got: {c})")