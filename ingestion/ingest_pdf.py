from .base_ingestor import BasePdfIngestor
from rag_module.config import (
    PDF_PATH_LSD,
    PDF_PATH_KTCT,
    PDF_PATH_TRIET,
    CHAPTER_PATTERN_LSD,
    CHAPTER_PATTERN_KTCT,
    CHAPTER_PATTERN_TRIET,
)


class LsdPdfIngestor(BasePdfIngestor):
    def __init__(self):
        super().__init__(
            path=PDF_PATH_LSD,
            chapter_pattern=CHAPTER_PATTERN_LSD,
            pdf_start=14,
            pdf_end=133,
        )

class KtctPdfIngestor(BasePdfIngestor):
    def __init__(self):
        super().__init__(
            path=PDF_PATH_KTCT,
            chapter_pattern=CHAPTER_PATTERN_KTCT,
        )
class TrietPdfIngestor(BasePdfIngestor):
    def __init__(self):
        super().__init__(
            path=PDF_PATH_TRIET,
            chapter_pattern=CHAPTER_PATTERN_TRIET,
        )

