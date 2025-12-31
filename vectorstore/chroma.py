# rag_module/vectorstore/chroma.py
from langchain_chroma import Chroma

class ChromaStore:
    def __init__(self, embed_model, persist_dir: str):
        self.embed_model = embed_model
        self.persist_dir = persist_dir
        self._store: Chroma | None = None

    def build(self, combined_docs):
        total_sections = sum(
            1 for d in combined_docs
            if d.metadata.get("type") in ["content", "content_trimmed", "bullet"] # Optinal: objective
        )
        total_objectives = sum(
            1 for d in combined_docs
            if d.metadata.get("type") == "objective"
        )
        print(f"Total sections in all chapters: {total_sections}")
        print(f"Total objectives in all chapters: {total_objectives}")
        print(f"Total docs: {len(combined_docs)}")

        if not combined_docs:
            print("Cảnh báo: Không có documents nào!")
            return None

        self._store = Chroma.from_documents(
            documents=combined_docs,
            embedding=self.embed_model,
            persist_directory=self.persist_dir,
        )
        return self._store

    def load(self):
        self._store = Chroma(
            embedding_function=self.embed_model,
            persist_directory=self.persist_dir,
        )
        return self._store

    @property
    def store(self) -> Chroma:
        if self._store is None:
            raise RuntimeError("Vectorstore chưa được build hoặc load.")
        return self._store
