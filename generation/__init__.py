from rag_module.llm import GeminiLLM
from .service import GenerationService



def get_generation_service(llm=None):
    
    llm = llm or GeminiLLM()
    return GenerationService(llm)