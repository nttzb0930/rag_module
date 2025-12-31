


def semantic_retrieve(
    vectorstore,
    questions,
    chapter_number,
    k
):
    results = []
    # search_kwags
    search_kwargs = {
        "k": k,
        "filter": {
            "$and": [
                {"type": {"$ne": "objective"}},
                {"chapter_number": str(chapter_number)}
            ]
        }
    }
    # init retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity"
        **search_kwargs,
    )
    # retriever với từng question
    for q in questions:
        results.extend(retriever.invoke(q))
    # return
    return results

def semantic_retrieve_with_scores(
    vectorstore,
    questions,
    chapter_number,
    k
):
    docs_all = []
    scores_all = []
    # search_kwargs
    search_kwargs = {
        "k": k,
        "filter": {
            "$and": [
                {"type": {"$ne": "objective"}},
                {"chapter_number": str(chapter_number)},
            ]
        },
    }
    # retriver với từng question
    for q in questions:
        results = vectorstore.similarity_search_with_score(
            q,
            k,
            filter= {
                "$and": [
                    {"type": {"$ne": "objective"}},
                    {"chapter_number": str(chapter_number)},
                ]
            }
        )
        for doc, score in results:
            docs_all.append(doc)
            scores_all.append(score)
    # return
    return docs_all, scores_all
