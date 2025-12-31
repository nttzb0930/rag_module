# rag_module/routing/parser.py

import json
import re


def parse_route_and_split(response: str):
    """
    Parse output từ LLM:
    - Chấp nhận JSON thuần
    - Chấp nhận JSON bọc ```json ... ```
    """

    if not response or not response.strip():
        raise ValueError("LLM trả về response rỗng")

    raw = response.strip()

    # 1️⃣ BÓC MARKDOWN CODE BLOCK NẾU CÓ
    # ```json ... ```
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if match:
        raw = match.group(1)

    # 2️⃣ PARSE JSON
    try:
        data = json.loads(raw)
    except Exception as e:
        raise ValueError(
            f"LLM output không phải JSON hợp lệ:\n{response}"
        ) from e

    # 3️⃣ VALIDATE STRUCTURE
    if not isinstance(data, dict):
        raise ValueError(f"JSON không phải object: {data}")

    chapter = data.get("chapter")
    questions = data.get("questions")

    if chapter is None:
        raise ValueError(f"Thiếu field 'chapter': {data}")

    if not questions or not isinstance(questions, list):
        raise ValueError(f"Field 'questions' không hợp lệ: {data}")

    # 4️⃣ NORMALIZE
    chapter = str(chapter).strip()
    if not chapter:
        raise ValueError(f"Giá trị 'chapter' trống sau normalize: {data}")
    questions = [q.strip() for q in questions if q and q.strip()]

    if not questions:
        raise ValueError("Danh sách câu hỏi rỗng sau khi normalize")

    return chapter, questions
