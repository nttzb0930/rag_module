from sentence_transformers import SentenceTransformer
from .settings import (
    DEFAULT_LLM_MODEL, 
    EMBED_MODEL_NAME,
    CHAPTER_PATTERN_LSD,
    CHAPTER_PATTERN_KTCT,
    CHAPTER_PATTERN_TRIET,
    NO_SPLIT_SECTION_PATH_LSD,
    PINECONE_INDEX,
)
from .paths import (
    PDF_PATH_LSD, 
    PDF_PATH_KTCT,
    PDF_PATH_TRIET,
    VECTORSTORE_DIR_LSD,
    VECTORSTORE_DIR_KTCT,
    VECTORSTORE_DIR_TRIET,
    COMBINED_DOCS_PATH_LSD,
    COMBINED_DOCS_PATH_KTCT,
    COMBINED_DOCS_PATH_TRIET,
    BM25_CACHE_PATH_LSD,
    BM25_CACHE_PATH_KTCT,
    BM25_CACHE_PATH_TRIET,
    SAMPLES_CACHE_PATH,
)
from .cors import (
    CORS_ALLOWED_ORIGINS,
    CORS_ALLOW_ORIGIN_REGEX,
)

class SentenceTransformerWrapper:
    """
    Adapter to provide both langchain embedding interface (embed_query/embed_documents)
    and direct encode() used by hybrid retrieval code.
    """
    def __init__(self, model):
        self.model = model

    def embed_query(self, text: str):
        return self.model.encode(text).tolist()

    def embed_documents(self, texts):
        return [self.model.encode(t).tolist() for t in texts]

    def encode(self, texts):
        return self.model.encode(texts)


_BASE_MODEL = SentenceTransformer(EMBED_MODEL_NAME, trust_remote_code=True)
EMBED_MODEL = SentenceTransformerWrapper(_BASE_MODEL)


__all__ = [
    "DEFAULT_LLM_MODEL",
    "EMBED_MODEL_NAME",
    "EMBED_MODEL",
    "PDF_PATH_LSD",
    "PDF_PATH_KTCT",
    "PDF_PATH_TRIET",
    "VECTORSTORE_DIR_LSD",
    "VECTORSTORE_DIR_KTCT",
    "VECTORSTORE_DIR_TRIET",
    "COMBINED_DOCS_PATH_LSD",
    "COMBINED_DOCS_PATH_KTCT",
    "COMBINED_DOCS_PATH_TRIET",
    "BM25_CACHE_PATH_LSD",
    "BM25_CACHE_PATH_KTCT",
    "BM25_CACHE_PATH_TRIET",
    "CHAPTER_PATTERN_LSD",
    "CHAPTER_PATTERN_KTCT",
    "CHAPTER_PATTERN_TRIET",
    "NO_SPLIT_SECTION_PATH_LSD",
    "PINECONE_INDEX",
    "SAMPLES_CACHE_PATH",
    "CORS_ALLOWED_ORIGINS",
    "CORS_ALLOW_ORIGIN_REGEX",
]
