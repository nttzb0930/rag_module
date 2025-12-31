import os

# llms/rag_module
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Thư mục dữ liệu & cache
DATA_DIR = os.path.join(BASE_DIR, "documents")         # PDF gốc
CACHE_DIR = os.path.join(BASE_DIR, "cache")            # cache *.pkl, bm25...

# Lịch sử Đảng (LSD)
PDF_PATH_LSD = os.path.join(DATA_DIR, "lsd.pdf")
VECTORSTORE_DIR_LSD = os.path.join(CACHE_DIR, "db_lsd")
COMBINED_DOCS_PATH_LSD = os.path.join(CACHE_DIR, "combined_docs_lsd.pkl")
BM25_CACHE_PATH_LSD = os.path.join(CACHE_DIR, "bm25_lsd_by_chapter.pkl")

# Kinh tế chính trị (KTCT)
PDF_PATH_KTCT = os.path.join(DATA_DIR, "ktct.pdf")
VECTORSTORE_DIR_KTCT = os.path.join(CACHE_DIR, "db_ktct")
COMBINED_DOCS_PATH_KTCT = os.path.join(CACHE_DIR, "combined_docs_ktct.pkl")
BM25_CACHE_PATH_KTCT = os.path.join(CACHE_DIR, "bm25_ktct_by_chapter.pkl")

# Triết học Mác Lenin (TRIET)
PDF_PATH_TRIET = os.path.join(DATA_DIR, "triethoc.pdf")
VECTORSTORE_DIR_TRIET = os.path.join(CACHE_DIR, "db_triet")
COMBINED_DOCS_PATH_TRIET = os.path.join(CACHE_DIR, "combined_docs_triet.pkl")
BM25_CACHE_PATH_TRIET = os.path.join(CACHE_DIR, "bm25_triet_by_chapter.pkl")


