# Cấu hình

Thư mục `config/` gom các cấu hình dùng chung cho toàn bộ pipeline RAG:

- model embedding và LLM
- regex tách chương
- đường dẫn PDF/cache/vector store
- tên Pinecone index
- wrapper cho embedding model

## `settings.py`

File này chứa các cấu hình hành vi của hệ thống.

### `EMBED_MODEL_NAME`

Tên embedding model đang dùng:

```python
EMBED_MODEL_NAME = "Alibaba-NLP/gte-multilingual-base"
```

Model này được dùng cho:

- Chroma vector store
- semantic retrieval
- hybrid retrieval
- Pinecone semantic answer cache

## `DEFAULT_LLM_MODEL`

Model Gemini mặc định:

```python
DEFAULT_LLM_MODEL = "models/gemini-2.5-flash"
```

Giá trị này được dùng bởi `llm/gemini.py` khi khởi tạo `GeminiLLM`.

## Regex tách chương

Ba biến regex dùng để tách chương theo từng tài liệu:

```python
CHAPTER_PATTERN_LSD
CHAPTER_PATTERN_KTCT
CHAPTER_PATTERN_TRIET
```

Ý nghĩa:

- `CHAPTER_PATTERN_LSD`: pattern cho Lịch sử Đảng.
- `CHAPTER_PATTERN_KTCT`: pattern cho Kinh tế chính trị.
- `CHAPTER_PATTERN_TRIET`: pattern cho Triết học Mác Lenin.

Các pattern này được truyền vào các class ingestor trong `ingestion/ingest_pdf.py`.

## `NO_SPLIT_SECTION_PATH_LSD`

Danh sách section đặc biệt của tài liệu Lịch sử Đảng:

```python
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
```

Mục đích là đánh dấu các section có format đặc biệt hoặc không nên split theo
rule mặc định.

## `PINECONE_INDEX`

Tên Pinecone index dùng cho semantic answer cache:

```python
PINECONE_INDEX = "ragmodule1"
```

Pinecone trong project này không lưu vector store chính của tài liệu. Vector
store tài liệu đang dùng Chroma trong `cache/db_*`. Pinecone chỉ dùng để tìm
câu hỏi cũ tương tự trong answer cache.

## `paths.py`

File này gom toàn bộ đường dẫn dữ liệu và cache.

### Đường dẫn gốc

```python
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(BASE_DIR, "documents")
CACHE_DIR = os.path.join(BASE_DIR, "cache")
```

Ý nghĩa:

- `BASE_DIR`: thư mục gốc của package `rag_module`.
- `PROJECT_ROOT`: thư mục cha của package.
- `DATA_DIR`: thư mục chứa PDF nguồn.
- `CACHE_DIR`: thư mục chứa cache sinh ra khi chạy.

## Đường dẫn theo corpus

Mỗi corpus có 4 nhóm path chính:

```python
PDF_PATH_*
VECTORSTORE_DIR_*
COMBINED_DOCS_PATH_*
BM25_CACHE_PATH_*
```

Ví dụ với `lsd`:

```python
PDF_PATH_LSD = os.path.join(DATA_DIR, "lsd.pdf")
VECTORSTORE_DIR_LSD = os.path.join(CACHE_DIR, "db_lsd")
COMBINED_DOCS_PATH_LSD = os.path.join(CACHE_DIR, "combined_docs_lsd.pkl")
BM25_CACHE_PATH_LSD = os.path.join(CACHE_DIR, "bm25_lsd_by_chapter.pkl")
```

Các corpus hiện có:

- `lsd`: Lịch sử Đảng
- `ktct`: Kinh tế chính trị
- `triet`: Triết học Mác Lenin

## `SAMPLES_CACHE_PATH`

Cache cho sample semantic router:

```python
SAMPLES_CACHE_PATH = os.path.join(CACHE_DIR, "samples_semantic.pkl")
```

## `__init__.py`

File này re-export config để các module khác import ngắn gọn:

```python
from rag_module.config import EMBED_MODEL, PINECONE_INDEX
```

Nó cũng khởi tạo embedding model:

```python
_BASE_MODEL = SentenceTransformer(EMBED_MODEL_NAME, trust_remote_code=True)
EMBED_MODEL = SentenceTransformerWrapper(_BASE_MODEL)
```

## `SentenceTransformerWrapper`

Wrapper này giúp cùng một embedding model dùng được ở nhiều nơi:

```python
def embed_query(self, text: str)
def embed_documents(self, texts)
def encode(self, texts)
```

Ý nghĩa:

- `embed_query()` và `embed_documents()` phục vụ interface của LangChain/Chroma.
- `encode()` phục vụ hybrid retrieval và Pinecone cache.

Lưu ý: `EMBED_MODEL` được khởi tạo ngay khi import `rag_module.config`, nên lần
startup đầu có thể mất thời gian và cần đủ tài nguyên máy.

## Pinecone và Redis answer cache

Class chính:

```python
PineconeEmbCache
```

Vị trí:

```text
vectorstore/pinecone.py
```

Khởi tạo trong `main.py`:

```python
redis_store_ans = RedisAnswerStore(
    redis_url=os.getenv("REDIS_URL"),
    prefix="lsd:",
)

pinecone_emb_ans = PineconeEmbCache(
    index_name=PINECONE_INDEX,
    embed_model=EMBED_MODEL,
    redis_store=redis_store_ans,
)
```

Các tham số của `PineconeEmbCache`:

```python
def __init__(
    self,
    index_name: str,
    embed_model,
    redis_store,
    threshold: float = 0.9,
    topk: int = 5,
)
```

Ý nghĩa:

- `index_name`: tên Pinecone index, hiện lấy từ `PINECONE_INDEX`.
- `embed_model`: embedding model dùng để embed câu hỏi.
- `redis_store`: Redis store chứa payload/câu trả lời thật.
- `threshold`: ngưỡng similarity để nhận cache hit, mặc định `0.9`.
- `topk`: số kết quả Pinecone lấy về khi query, mặc định `5`.

## Luồng cache

Khi kiểm tra cache:

1. Embed câu hỏi bằng `EMBED_MODEL`.
2. Query Pinecone với `top_k=topk`.
3. Filter Pinecone theo `scope`.
4. Nếu best score nhỏ hơn `threshold`, bỏ qua cache.
5. Nếu đạt ngưỡng, lấy `id` tốt nhất.
6. Dùng `id` đó để đọc answer thật từ Redis.

Khi lưu cache:

1. Sinh `_id` mới.
2. Lưu payload vào Redis.
3. Embed câu hỏi.
4. Upsert vector vào Pinecone.

Payload Redis:

```python
{
    "question": question,
    "answer": answer,
    "created_at": now,
}
```

Metadata Pinecone:

```python
{
    "created_at": now,
    "scope": scope,
}
```

## Lưu ý hiện tại

Redis prefix đang hard-code trong `main.py`:

```python
prefix="lsd:"
```

Trong khi Pinecone metadata có `scope` cho từng corpus. Nếu muốn cache tách
rõ cho `lsd`, `ktct`, `triet`, nên đưa Redis prefix vào config hoặc tạo store
theo từng corpus.
