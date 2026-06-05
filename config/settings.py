EMBED_MODEL_NAME = "Alibaba-NLP/gte-multilingual-base"
DEFAULT_LLM_MODEL = "models/gemini-3.1-flash-lite"
CHAPTER_PATTERN_LSD = r"CHƯƠNG\s+\d+:.*?(?=\nMỤC|\nCHƯƠNG\s+\d+:|$)"
CHAPTER_PATTERN_KTCT = r"(?ms)^\s*CHƯƠNG\s+[IVXLC\d]+.*?(?=^\s*CHƯƠNG\s+[IVXLC\d]+|\n\s*MỤC|\Z)"
CHAPTER_PATTERN_TRIET = r"(?ms)^\s*CHƯƠNG\s+[IVXLC\d]+.*?(?=\nMỤC|\nCHƯƠNG\s+\d+:|$)"
NO_SPLIT_SECTION_PATH_LSD = {
        "2.1.1.2",
        "2.2.1.1",
        "3.2.1.2",
        "3.2.2.1",
        "3.2.2.2",
        "3.2.2.3",
        "3.2.2.4",
        "3.2.2.5",
}
PINECONE_INDEX = 'ragmodule1'



