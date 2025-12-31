
def debug_tokenize(model, docs):
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained("Alibaba-NLP/gte-multilingual-base")

    # Lấy list text
    docs = [d.page_content for d in combined_docs]

    # Batch tokenize: không truncate, không padding
    encodings = tokenizer(
        docs,
        padding=False,
        truncation=False,
        return_length=True
    )

    token_lengths = encodings["length"]
    limit = tokenizer.model_max_length  # 8192
    print("===== TOKEN LENGTH REPORT =====")
    for idx, length in enumerate(token_lengths):
        if length > limit:
            print(f"Doc {idx} vượt {length} tokens → sẽ bị TRUNCATE khi embed")
        else:
            print(f"Doc {idx} OK ({length} tokens)")
debug_tokenize(combined_docs)