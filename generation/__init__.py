from rag_module.llm import GeminiLLM
from .service import GenerationService



def get_generation_service(llm=None):
    if llm is None:
        llm = GeminiLLM()
    return GenerationService(llm)