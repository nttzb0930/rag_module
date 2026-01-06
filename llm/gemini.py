from google import genai
from rag_module.llm.base import BaseLLM
from rag_module.config import DEFAULT_LLM_MODEL
import os
from dotenv import load_dotenv
load_dotenv()




class GeminiLLM(BaseLLM):
    def __init__(self, model=DEFAULT_LLM_MODEL):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GOOGLE_API_KEY is missing. Set it in environment or .env file."
            )

        self.model = model
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """
        prompt template, question or anything
        """
        response = self.client.models.generate_content(model=self.model,contents=prompt)
        return response.text
    def stream(self, prompt: str):
        """
        prompt template, question or anything
        Yield text từng chunk dùng với StreamingResponse
        """
        response = self.client.models.generate_content_stream(model=self.model,contents=prompt)
        for chunk in response:
            if not chunk.candidates:
                continue
            candidate = chunk.candidates[0]
            for part in candidate.content.parts:
                text = getattr(part, "text", None)
                if text:
                    yield text