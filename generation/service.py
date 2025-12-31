from .prompts import ANSWER_PROMPT, SUMMARIZE_PROMPT


class GenerationService:
    def __init__(self, llm):
        self.llm = llm

    @staticmethod
    def _build_context(docs):
        return "\n\n".join(d.page_content for d in docs)
    

    def answer(self, question, docs):
        prompt = ANSWER_PROMPT.format(
            context=self._build_context(docs),
            question=question,
        )
        return self.llm.generate(prompt)

    
    def summarize(self, question, docs):
        prompt = SUMMARIZE_PROMPT.format(
            context=self._build_context(docs),
            question=question,
        )
        return self.llm.generate(prompt)


    def stream(self, question, docs):
        prompt= ANSWER_PROMPT.format(
            context=self._build_context(docs),
            question=question,
        )
        for chunk in self.llm.stream(prompt):
            yield chunk




# def generate_answer(question, docs, llm):
#     context = "\n\n".join(d.page_content for d in docs)
#     prompt = ANSWER_PROMPT.format(
#         context=context,
#         question=question
#     )
#     return llm.generate(prompt)

# def generate_summarize_answer(question, docs, llm):
#     context = "\n\n".join(d.page_content for d in docs)
#     prompt = SUMMERIZE_PROMPT.format(
#         context=context,
#         question=question
#     )
#     return llm.generate(prompt)
# def generate_answer_stream(question, docs, llm):
#     context = "\n\n".join(d.page_content for d in docs)
#     prompt = ANSWER_PROMPT.format(question=question,context=context)
#     # stream từ LLM
#     for chunk in llm.stream(prompt):
#         yield chunk