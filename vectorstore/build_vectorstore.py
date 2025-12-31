import os
from rag_module.config import (
    EMBED_MODEL,
    VECTORSTORE_DIR_LSD,
    VECTORSTORE_DIR_KTCT,
    VECTORSTORE_DIR_TRIET,
)
from rag_module.ingestion import (
    load_or_build_lsd,
    load_or_build_ktct,
    load_or_build_triet,
)
from .chroma import ChromaStore


def load_or_build_lsd_vectorstore():
    # Nếu có folder db rồi thì chỉ load
    if os.path.isdir(VECTORSTORE_DIR_LSD):
        store = ChromaStore(EMBED_MODEL, VECTORSTORE_DIR_LSD)
        return store.load()

    # Nếu chưa có thì build corpus + build vectorstore
    docs, _ = load_or_build_lsd()
    store = ChromaStore(EMBED_MODEL, VECTORSTORE_DIR_LSD)
    return store.build(docs)


def load_or_build_ktct_vectorstore():
    if os.path.isdir(VECTORSTORE_DIR_KTCT):
        store = ChromaStore(EMBED_MODEL, VECTORSTORE_DIR_KTCT)
        return store.load()

    docs, _ = load_or_build_ktct()
    store = ChromaStore(EMBED_MODEL, VECTORSTORE_DIR_KTCT)
    return store.build(docs)


def load_or_build_triet_vectorstore():
    if os.path.isdir(VECTORSTORE_DIR_TRIET):
        store = ChromaStore(EMBED_MODEL, VECTORSTORE_DIR_TRIET)
        return store.load()
    

    docs, _ = load_or_build_triet()
    store = ChromaStore(EMBED_MODEL, VECTORSTORE_DIR_TRIET)
    return store.build(docs)