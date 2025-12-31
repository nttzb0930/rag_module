from rag_module.prompts import ROUTER_AND_SPLIT_PROMPT
from rag_module.llm import GeminiLLM
from .parser import parse_route_and_split


def route_and_split(question: str, chapter_titles: list[str]):
    llm = GeminiLLM()
    chapters_text = "\n".join(f"{i+1}. {title}" for i, title in enumerate(chapter_titles))
    prompt = ROUTER_AND_SPLIT_PROMPT.format(
        chapters=chapters_text,
        question=question,
    )

    response = llm.generate(prompt)
    chapter_number, sub_questions = parse_route_and_split(response)


    print(f"{'-'*100}\n"
          f"[DEBUG] Routed chapter: {chapter_number}\n"
          f"[DEBUG] Sub-questions: {len(sub_questions)}\n"
          f"{'-'*100}")
    for i, sq in enumerate(sub_questions, start=1):
        print(f"  [{i}] {sq}")
    print("-"*100)
    return chapter_number, sub_questions
