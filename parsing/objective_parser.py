from langchain_core.documents import Document
import re
# Thấy mục tiêu chương có 3 phần kiến thức tư tưởng kĩ năng tách làm 3 sau làm gì thì làm
def split_objectives(text):
    """
    Tách mục tiêu chương từ text thành 3 phần:
    - knowledge
    - thought
    - skill
    """
    sections = {
        "knowledge": "",
        "thought": "",
        "skill": ""
    }

    # Regex nhận dạng từng mục
    patterns = {
        "knowledge": r"Về\s+kiến\s+thức\s*[:：]\s*(.*?)(?=Về\s+tư\s+tưởng|Về\s+kỹ\s+năng|$)",
        "thought": r"Về\s+tư\s+tưởng\s*[:：]\s*(.*?)(?=Về\s+kỹ\s+năng|$)",
        "skill": r"Về\s+kỹ\s+năng\s*[:：]\s*(.*)$"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.DOTALL)
        if match:
            # Làm sạch nội dung
            cleaned = match.group(1).strip()
            cleaned = re.sub(r"\s+", " ", cleaned)
            sections[key] = cleaned

    return sections
# Sau khi tách xong chuyển thành docs
def objectives_to_documents(summary_text, chapter_number: str, chapter_title: str, source: str):
    parts = split_objectives(summary_text)
    documents = []
    chapter_str = str(chapter_number)
    for key, content in parts.items():
        if not content:
            continue
        
        metadata = {
            "type": "objective",           # loại tài liệu
            "objective_type": key,         # knowledge / thought / skill
            "chapter_number": chapter_str,
            "chapter_title": chapter_title,
            "title": f"Mục tiêu ({key}) - Chương {chapter_str}",
            "source": f"{source}",
            "content_length": len(content)
        }

        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)

    return documents