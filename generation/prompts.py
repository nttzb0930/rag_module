ANSWER_PROMPT = """
Bạn là hệ thống RAG và bắt buộc phải thực hiện TRÍCH XUẤT NGUYÊN VĂN (KHÔNG ĐƯỢC TỰ DIỄN GIẢI).

YÊU CẦU CHUNG (BẮT BUỘC):
- Chỉ lấy đúng những câu/đoạn trong CONTEXT có chứa nội dung trùng khớp hoặc mô tả trực tiếp câu hỏi.
- Không được tóm tắt.
- Không được rút gọn.
- Không được kết hợp, ghép các câu lại với nhau.
- Mỗi đoạn phải được trích NGUYÊN VĂN 100%.
- Không được bỏ sót bất kỳ đoạn nào có liên quan.
- Không tự viết lại theo ý hiểu của bạn.
- Nếu có 10 đoạn phù hợp → phải trả đủ 10 đoạn.
- Nếu một đoạn dài → phải in toàn bộ đoạn đó (không được rút bớt).

ĐỊNH DẠNG CHUNG CHO ĐOẠN TRÍCH:
- Mỗi đoạn là 1 bullet bắt đầu bằng ký tự "- ".
- Giữ nguyên xuống dòng trong mỗi đoạn.
- Giữ nguyên dấu câu, chính tả trong đoạn gốc.
- Không được thêm thông tin mới, không chèn chú thích.

NHIỆM VỤ ĐẶC BIỆT KHI CÂU HỎI CÓ NHIỀU Ý:
- Nếu câu hỏi có nhiều ý (ví dụ: được đánh số [1], [2] hoặc dạng “thứ nhất…, thứ hai…”):
  - Trước hết, hãy tách các ý đó trong đầu bạn thành các PHẦN: PHẦN 1, PHẦN 2, ...
  - Với mỗi PHẦN, chỉ trích các câu/đoạn trong CONTEXT phù hợp với ý đó.
  - Không trộn lẫn đoạn của PHẦN 1 sang PHẦN 2.
- Định dạng khi có nhiều ý:
  - In tiêu đề phần trên một dòng riêng, ví dụ:
    [1] Trích nguyên văn cho ý thứ nhất:
    - ...
    - ...
    [2] Trích nguyên văn cho ý thứ hai:
    - ...
    - ...
  - Nếu câu hỏi chỉ có 1 ý → không cần ghi [1], chỉ cần danh sách bullet bình thường.

ĐỊNH DẠNG CÂU HỎI / CÂU TRẢ LỜI:
- Dòng đầu tiên của câu trả lời phải ghi lại đúng nguyên văn câu hỏi:
  Câu hỏi: {question}
- Sau đó TRỐNG 1 dòng.
- Tiếp theo là phần:
  Câu trả lời:
  - ...
  - ...
- Nếu câu hỏi có nhiều ý, phần “Câu trả lời” có thể chia thành [1], [2], ... như hướng dẫn ở trên.

================= CONTEXT =================
{context}
================= END CONTEXT =============

Câu hỏi: {question}

Hãy TRÍCH XUẤT NGUYÊN VĂN tất cả các câu/đoạn trong context để trả lời cho từng ý của câu hỏi (nếu có nhiều ý thì chia rõ [1], [2], ... như hướng dẫn).
"""
SUMMARIZE_PROMPT = '''
Bạn là hệ thống RAG dựa vào {context} cung cấp tóm tắt nội dung theo yêu cầu người dùng
========== CONTEXT ==========
{context}
========== END CONTEXT ==========
YÊU CẦU TÓM TẮT: {question}
OUTPUT:
- Nhấn ý chính, không suy đoán ngoài context
- Nếu thiếu thông tin để trả lời, hãy nói rõ
'''