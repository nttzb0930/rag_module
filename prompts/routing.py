ROUTER_AND_SPLIT_PROMPT = """
Bạn có 2 nhiệm vụ:

==========================
NHIỆM VỤ 1: XÁC ĐỊNH CHƯƠNG
==========================
Dựa vào danh sách chương sau:
{chapters}

Hãy xác định câu hỏi thuộc chương nào.
Chỉ trả lời số chương  
KHÔNG được giải thích.

==========================
NHIỆM VỤ 2: TÁCH CÂU HỎI
==========================
Tách câu hỏi thành 1–4 câu hỏi con, mỗi câu chỉ chứa **1 yêu cầu duy nhất**.  
Nếu câu chỉ có 1 nội dung → giữ nguyên, không tách.

Trả lời JSON với dạng:
{{
  "chapter": <số chương>,
  "questions": ["câu hỏi 1", "câu hỏi 2", ...]
}}

==========================
Câu hỏi gốc: "{question}"
==========================
"""
