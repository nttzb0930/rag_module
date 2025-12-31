# rag_module/ingestion/corpus_build.py
import os
import pickle

from .ingest_pdf import KtctPdfIngestor, LsdPdfIngestor, TrietPdfIngestor
from rag_module.config import COMBINED_DOCS_PATH_LSD, COMBINED_DOCS_PATH_KTCT, COMBINED_DOCS_PATH_TRIET


class CorpusCache:
    def __init__(self, ingestor, cache_path: str):
        self.ingestor = ingestor
        self.cache_path = cache_path

    def load_or_build(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "rb") as f:
                combined_docs, chapter_titles= pickle.load(f)
        else:
            combined_docs, chapter_titles = self.ingestor.ingest()
            with open(self.cache_path, "wb") as f:
                pickle.dump((combined_docs, chapter_titles), f)
        return combined_docs, chapter_titles
def load_or_build_lsd():
    return CorpusCache(LsdPdfIngestor(), COMBINED_DOCS_PATH_LSD).load_or_build()


def load_or_build_ktct():
    return CorpusCache(KtctPdfIngestor(), COMBINED_DOCS_PATH_KTCT).load_or_build()


def load_or_build_triet():
    return CorpusCache(TrietPdfIngestor(), COMBINED_DOCS_PATH_TRIET).load_or_build()



