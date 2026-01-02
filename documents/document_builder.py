from langchain_core.documents import Document
from rag_module.parsing import extract_star_bullets
import json

# Convert To Documents 
def sections_to_documents_with_bullets(sections, doc_type: str, chapter_number: str, chapter_title: str):
    """
    sections: lấy từ numbered_section_parser
    doc_type: "type": "content (bullet, content_trimmed,objective)
    chapter_number:
    chapter_title 
    Nếu không có content (chính là title của các sections) -> pass
    Nếu có content:
        Tách thử bullet xem có không
        Nếu không có thì tạo docs với nguyên đoạn (if not bullets) với metadata -> pass
        Nếu có xây docs cho bulllet với metadata mới được thêm
        Sau khi tách bullet title và content khỏi section nếu còn thì đưa nó vào docs với type content_trimmed
    """
    documents = []
    # sections = {"number", "title", "content", "level"}
    for item in sections:
        content = item.get("content", "").strip()
        if not content:
            continue

        number = item["number"]
        parent_path = item["path"]

        # Base Metadata
        base_metadata = {
            "type": doc_type,
            "number": number,
            "title": item["title"],
            "level": item["level"],
            "parent": item.get("parent"),
            "root": item.get("root"),
            "path": json.dumps(parent_path),
            "section_title": item.get("section_title"),
            "chapter_title": chapter_title,
            "chapter_number": chapter_number,
            "source": item.get("source"),
        }

        # Tách Theo Star Bullet
        bullets = extract_star_bullets(content, parent_path, section_path=number)
        # Return Bullets Format List[Dict]
        # Nếu Không Có Star Bullet → Giữ Nguyên Section Đó
        if not bullets:
            meta = base_metadata.copy()
            meta["content_length"] = len(content)
            documents.append(Document(page_content=content, metadata=meta))
            continue

        # Nếu Có Star Bullet → Tách Với Từng Star Bullet Và Tạo Doc
        remaining = content

        for b in sorted(bullets, key=lambda x: x["start"], reverse=True):
            # print("\n--- DEBUG BULLET ---")
            # print("Bullet index:", b["bullet_index"])
            # print("Start:", b["start"])
            # print("End:", b["end"])
            # print("Extracted bullet content:", repr(b["bullet_content"][:1]))
            # print("---------------------\n")

            bullet_meta = base_metadata.copy()
            bullet_meta.update({
                "type": "bullet",
                "bullet_index": b["bullet_index"],
                "bullet_title": b["bullet_title"],
                "content_length": len(b["bullet_content"]),

                # Thêm bullet_path (Nhánh Con)
                "bullet_path": json.dumps(parent_path + [f"bullet_{b['bullet_index']}"])
            })

            documents.append(
                Document(
                    page_content=b["bullet_content"], # lấy lại content đã cut từ trước
                    metadata=bullet_meta # update lại metadata
                )
            )

            # Loại Bỏ Đoạn Star Bullet Trong Section Gốc
            remaining = remaining[:b["start"]] + remaining[b["end"]:]

        # Phần Còn Lại Của Section Sau Khi Cắt Star Bullet
        cleaned = remaining.strip()
        if cleaned:
            meta_trim = base_metadata.copy()
            meta_trim["type"] = "content_trimmed"
            meta_trim["content_length"] = len(cleaned)

            documents.append(Document(page_content=cleaned, metadata=meta_trim))

    return documents
