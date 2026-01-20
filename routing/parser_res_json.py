# rag_module/routing/parser.py

import json
import re


def parse_json(res: str):
    """
    Parse output từ res llm
    - Json thuần hoặc bọc ```json ...```
    """
    if not res or not res.strip():
        raise ValueError("Không tìm thấy response trả về từ llm")
    raw = res.strip()

    # Remove Markdown
    match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", raw, re.DOTALL)
    if match:
        raw = match.group(1)
    else:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            raw = raw[start:end+1]

    # Fix double braces
    """
    {{
        "chapter": 2,
        "questions": ["Diễn biến toàn quốc kháng chiến diễn ra như thế nào?"]
    }}
    """
    raw = raw.replace('{{', '{').replace('}}', '}')
    # Parse Json
    try:
        data = json.loads(raw)  
    except Exception as e:
        raise ValueError(
            f"LLM output không phải JSON hợp lệ:\n{res}"
        ) from e
    # Validate Structure
    if not isinstance(data, dict):
        raise ValueError(f"JSON không phải object: {data}")
    return data
    

def parse_route_and_split(res: str):
    data = parse_json(res)


    chapter = data.get("chapter")
    questions = data.get("questions")
    if chapter is None:
        raise ValueError(f"Thiếu field 'chapter': {data}")
    chapter = str(chapter).strip()
    if not chapter:
        raise ValueError(f"Giá trị 'chapter' trống sau normalize: {data}")
    
    questions = [q.strip() for q in questions if q and q.strip()]
    if not questions or not isinstance(questions, list):
        raise ValueError(f"Field 'questions' không hợp lệ: {data}")
    if not questions:
        raise ValueError("Danh sách câu hỏi rỗng sau khi normalize")

    return chapter, questions


def parse_intent_response(res: str):
    data = parse_json(res)
    user_input = data.get('user_input')
    intent = data.get("intent")
    need_more_information = bool(data.get("need_more_information"))
    needs_normalization = bool(data.get("needs_normalization"))
    normalized_query = (data.get("normalized_query") or "").strip()
    sub_questions = data.get("sub_questions") or []
    answer = data.get("answer") or ""
    if intent is None:
        raise ValueError(f"Thiếu field 'intent': {data}")
    if not isinstance(sub_questions, list):
        raise ValueError(f"Field 'sub_questions' không hợp lệ: {data}")
    return user_input, intent, need_more_information, needs_normalization, normalized_query, sub_questions, answer

def parse_corpus_response(res: str):
    data = parse_json(res)
    corpus = data.get('corpus')
    if not corpus:
        raise ValueError("Không xác định được corpus")
    return corpus