# RAG Module

RAG Module là service FastAPI dùng để trả lời câu hỏi học tập dựa trên các
tài liệu PDF cục bộ. Dự án đọc tài liệu, tách nội dung thành các document có
metadata, build cache và vector store, route câu hỏi đến đúng môn/chương, truy
xuất context liên quan rồi sinh câu trả lời bằng Gemini.

## Tính năng

- Ingest PDF cho 3 corpus: `lsd`, `ktct`, `triet`.
- Tách chương, mục tiêu, section, bullet và build metadata.
- Cache corpus đã xử lý trong `cache/*.pkl`.
- Lưu vector store Chroma trong `cache/db_*`.
- Retrieval kết hợp semantic search, BM25, deduplication và MMR.
- Route intent cho câu hỏi học tập, chitchat và general QA.
- Cache câu trả lời bằng Pinecone embeddings và Redis.
- Cung cấp API FastAPI qua endpoint `/rag`.

## Cấu trúc dự án

```text
rag_module/
  main.py                 # FastAPI app và endpoint /rag
  pipeline.py             # Điều phối RAG và summary pipeline
  config/                 # Đường dẫn, settings, embedding model
  ingestion/              # Ingest PDF và build/load corpus cache
  loaders/                # PDF loader
  raw_text/               # Helper trích xuất raw text
  parsing/                # Parser chương, mục tiêu, section, bullet
  text_preprocess/        # Làm sạch text và sửa heading
  documents/              # Chuyển dữ liệu thành LangChain Document
  vectorstore/            # Tích hợp Chroma, Pinecone, Redis
  retrieval/              # Semantic, BM25, hybrid, dedup, rerank
  routing/                # Route intent, corpus, chapter, sub-question
  generation/             # Prompt và service gọi LLM
  llm/                    # Adapter cho LLM
  utils/                  # Helper dùng chung cho parse/format answer
  debug/                  # Helper debug
  documents/              # PDF nguồn
  cache/                  # Cache sinh ra trong quá trình chạy
```

## Yêu cầu

Khuyến nghị dùng Python 3.10 trở lên.

Các package chính được project sử dụng:

```text
fastapi
uvicorn
pydantic
python-dotenv
google-genai
sentence-transformers
langchain-core
langchain-community
langchain-chroma
rank-bm25
scikit-learn
numpy
redis
pinecone
```

Dependency của project được khai báo trong `pyproject.toml`.

## Cài đặt

Tạo và kích hoạt virtual environment, sau đó cài project ở chế độ editable:

```bash
cd C:\Users\nttzb\Downloads\rag_module
pip install -e .
```

Nếu cần cài thêm dependency phục vụ test/dev:

```bash
pip install -e ".[dev]"
```

## Biến môi trường

Tạo file `.env` từ file mẫu:

```bash
copy .env.example .env
```

Sau đó điền giá trị thật:

```env
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
REDIS_URL=redis://localhost:6379
DEBUG_RANKING=false
```

Trong đó:

- `GOOGLE_API_KEY`: dùng để gọi Gemini.
- `PINECONE_API_KEY`: dùng cho cache câu trả lời bằng embedding.
- `REDIS_URL`: dùng cho Redis answer store.
- `DEBUG_RANKING`: bật/tắt log debug ranking.

Không commit file `.env` thật. Chỉ commit `.env.example`.

## Cấu hình

Cấu hình chính nằm trong thư mục config/, bao gồm model, regex tách chương, đường dẫn PDF/cache/vector store và tên Pinecone index.

Chi tiết xem [config/README.md](config/README.md).

## Chạy API

Chạy từ thư mục cha của `rag_module`:

```bash
cd C:\Users\nttzb\Downloads
uvicorn rag_module.main:app --reload
```

Nếu đã cài bằng `pip install -e .`, bạn cũng có thể chạy lệnh `uvicorn` từ
thư mục project.

Mở Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Nếu cần expose trong LAN:

```bash
uvicorn rag_module.main:app --host 0.0.0.0 --port 8000 --reload
```

## API

### POST `/rag`

Request:

```json
{
  "question": "Trình bày nội dung cơ bản của chương 1"
}
```

Response:

```json
{
  "answer": "..."
}
```

## Luồng xử lý

Khi API startup, `main.py` khởi tạo:

1. Redis answer store.
2. Pinecone embedding answer cache.
3. Gemini generation service.
4. Corpus cache cho `lsd`, `ktct`, `triet`.
5. Chroma vector store cho từng corpus.

Với mỗi request `/rag`, hệ thống xử lý theo thứ tự:

1. `routing.intent_route()` xác định intent của câu hỏi.
2. `select_corpus()` chọn corpus phù hợp bằng rule hoặc LLM routing.
3. `route_and_split()` xác định chapter và tách sub-question.
4. Kiểm tra cache câu trả lời trong Pinecone/Redis.
5. `retrieval.retrieve_documents()` lấy context bằng semantic/BM25/hybrid retrieval.
6. `generation.GenerationService` build prompt và gọi Gemini.
7. `utils.answer` parse và format câu trả lời cuối.

## Dữ liệu và cache

PDF nguồn nằm trong thư mục `documents/`.

Các file sinh ra trong quá trình chạy nằm trong `cache/`, ví dụ:

- `combined_docs_*.pkl`
- `bm25_*_by_chapter.pkl`
- `db_*` Chroma vector store

Khi cache bị thiếu, các loader trong `ingestion` và `vectorstore` có thể build
lại từ PDF nguồn.

## Lưu ý phát triển

- Chạy API từ thư mục cha để `rag_module` được import như một package.
- Không commit `.env` thật.
- Không commit thay đổi trong `cache/db_*` nếu không cố ý cập nhật vector store.
- File entrypoint FastAPI là `main.py`, chạy bằng `rag_module.main:app`.
- Các helper parse/format answer nằm trong `utils/answer.py`.
