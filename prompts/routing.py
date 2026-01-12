ROUTE_CORPUS_PROMPT = """
NHIỆM VỤ CHÍNH: PHÂN LOẠI CÂU HỎI THUỘC MÔN:
- lsd: Lịch Sử Đảng
- ktct: Kinh Tế Chính Trị Mác Lê Nin
- triet: Triết Học Mác Lê Nin
LUỒNG THỰC HIỆN:
- Dựa vào: {question} 
- Xác định xem câu hỏi của người dùng có liên quan đến môn học không
- Nếu có xác định {question} thuộc môn học nào trả lại
    OUTPUT: CHỈ TRẢ VỀ ĐỊNH DẠNG CHUẨN JSON DƯỚI ĐÂY KHÔNG GIẢI THÍCH GÌ THÊM 
    ```json
    {{
        "corpus": lsd|ktct|triet
    }}
- Nếu không xác định được {question} có liên quan đến những môn học đã đề cập trả lại
   OUTPUT: CHỈ TRẢ VỀ ĐỊNH DẠNG CHUẨN JSON DƯỚI ĐÂY KHÔNG GIẢI THÍCH GÌ THÊM
   ```json
   {{
      "corpus": "unknown"
   }}
"""
ROUTE_CHAPTER_NUMBER_and_SPLIT_QUES_PROMPT = """
NHIỆM VỤ CỦA BẠN LÀ:
//
NHIỆM VỤ 1: XÁC ĐỊNH LẠI CÂU HỎI NGƯỜI DÙNG
Dựa vào câu hỏi sau:
{question}
- Xác định xem câu hỏi có chính xác đã liên quan đến môn học
   +) lsd: Lịch Sử Đảng
   +) ktct: Kinh Tế Chính Trị Mác Lê Nin
   +) triet: Triết Học Mác Lê Nin
- Với những câu hỏi thông thường có thể trả lời ngay
- Nếu đã xác định được câu hỏi thuộc môn học nào thì tiếp tục làm các nhiệm vụ phía dưới
//
NHIỆM VỤ 2: XÁC ĐỊNH CHƯƠNG
Dựa vào danh sách chương sau:
{chapters}
- Hãy xác định câu hỏi thuộc chương nào
- Chỉ trả lời số chương
- KHÔNG giải thích gì thêm.
//
NHIỆM VỤ 3: TÁCH CÂU HỎI
Dựa vào câu hỏi sau:
{question}
- Tách câu hỏi thành 1–4 câu hỏi con, mỗi câu chỉ chứa **1 yêu cầu duy nhất**.  
- Nếu câu chỉ có 1 nội dung → giữ nguyên, không tách.
- Nếu câu có nhiều nội dung:
1. Mỗi sub-question phải tự đủ nghĩa (self‑contained)
2. Không dùng “đó/này/việc này/điều này/đường lối đó…”.
3. Nếu câu có “đó/này” thì phải thay bằng cụm danh từ đầy đủ từ câu trước (vd: “đường lối cách mạng hai miền trong Đại hội III”).
4. Câu hỏi phải đúng dạng câu hỏi
5. Nếu là “ý nghĩa” thì phải viết dạng: Ý nghĩa của ... là gì?
6. Luôn kết thúc bằng ? (không trả “cụm danh từ” trơ trọi).
//
OUTPUT: 
- Trả lời JSON với dạng:
{{
  "chapter": <số chương>,
  "questions": ["câu hỏi 1", "câu hỏi 2", ...]
}}

"""


ROUTE_INTENT_PROMPT = """
Bạn là bộ phân loại truy vấn đầu vào cho hệ thống hỏi đáp.

NHIỆM VỤ
Phân loại input của người dùng vào MỘT trong các intent sau:

1. "chitchat"
   - Trò chuyện xã giao, cảm xúc, hỏi han
   - Ví dụ: chào hỏi, cảm ơn, nói chuyện phiếm

2. "general_qa"
   - Câu hỏi kiến thức phổ thông
   - Có thể trả lời trực tiếp bằng kiến thức chung
   - KHÔNG yêu cầu tra cứu tài liệu học tập, môn học hay chương cụ thể
   - Ví dụ: thiên văn, lịch, địa lý, đời sống, khoa học thường thức

3. "study"
   - Câu hỏi học tập cần tra cứu trong bộ tài liệu/môn học
   - Thường liên quan đến: bài học, chương, khái niệm học thuật, công thức
   - Ví dụ: “giải thích TCP”, “định luật Ôm”, “trong chương này…”

4. "summary"
   - Yêu cầu tóm tắt, hệ thống hóa kiến thức
   - Có thể coi là một dạng đặc biệt của study
   - Ví dụ: "tóm tắt", "tóm tắt", "tóm lược", "viết tóm tắt", "ý chính",
        "tóm tắt",
        "tóm lược",
        "viết tóm tắt",
        "tóm tắt giúp mình",
        "tóm tắt giúp tôi",
        "tóm tắt lại",
        "tóm tắt nội dung",
        "tóm tắt phần này",
        "tóm tắt đoạn này",
        "ý chính",
        "ý cơ bản",
        "ý trọng tâm",
        "nội dung chính",
        "các ý chính",
---
Nếu intent là "study" hoặc "summary":
- Kiểm tra câu hỏi có đủ thông tin để trả lời chưa
- Nếu đủ -> đặt "need_more_information": false
- Nếu thiếu → đặt "need_more_information": true
- KHÔNG tự suy đoán hoặc điền thêm thông tin
---
Nếu intent là "general_qa" hoặc "chitchat":
- Được phép trả lời ngay nhưng không quá dài dòng.
CHUẨN HÓA CÂU HỎI
- Chỉ chuẩn hóa nếu intent là "study_rag" hoặc "summary"
- Chỉ chuẩn hóa nếu câu hỏi:
  - dài
  - nhiều ý
  - có văn nói, từ thừa
- Nếu câu hỏi ngắn, 1 ý rõ → KHÔNG chuẩn hóa
- Nếu câu hỏi có need_more_information: true thì chưa chuẩn hóa câu hỏi vội đợi người dùng bổ sung
- Có thể trả lời lại người dùng dựa vào question người dùng đã hỏi để bổ sung thông tin
CHUẨN HÓA BAO GỒM
- Viết lại câu hỏi ngắn gọn, rõ nghĩa
- Giữ nguyên thuật ngữ học thuật
- Nếu có nhiều ý, tách thành các sub_questions độc lập

---

CÁC RÀNG BUỘC (RẤT QUAN TRỌNG)
- KHÔNG xác định môn học
- KHÔNG xác định chương
- KHÔNG giải thích
- KHÔNG suy đoán ngoài input
- CHỈ trả về JSON hợp lệ

---



INPUT:
{{user_input}}

OUTPUT JSON:
{
  "user_input": {{user_input}}
  "intent": "...",
  "need_more_information: true|false,
  "needs_normalization": true | false,
  "normalized_query": "...",
  "sub_questions": [],
  "answer": ""
}
"""