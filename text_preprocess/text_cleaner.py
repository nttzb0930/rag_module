import re
def clean_text(text):
    """
    - Xóa số trang (10, 11, 12…)
    - Xóa header/footer rác
    - Gom dòng PDF bị tách
    - Xóa khoảng trắng lớn
    - Giữ nguyên format câu, không phá tiếng Việt
    - Chuẩn bị cho parser tách heading
    """

    # 1) Cắt theo dòng
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        raw = line.strip()

        # Bỏ dòng là số trang
        if re.fullmatch(r"\d{1,3}", raw):
            continue

        # Bỏ dòng chỉ toàn số + khoảng trắng
        if re.match(r"^\s*\d{1,3}\s*$", line):
            continue

        # Bỏ dòng hoàn toàn trống
        if raw == "":
            continue

        cleaned.append(raw)

    # Sau khi làm sạch từng dòng
    text = "\n".join(cleaned)

    # 2) Xóa khoảng trắng lớn trong nội bộ dòng
    text = re.sub(r"[ \t]{2,}", " ", text)

    # 3) Ghép các dòng bị xuống dòng giữa câu (PDF bug)
    #   Nếu dòng tiếp theo bắt đầu bằng chữ thường → nối vào dòng trước
    text = re.sub(
        r"(?<![\.\:\?])\n(?=[a-zà-ỹ“])",
        " ",
        text
    )

    # 4) Fix xuống dòng giữa ngoặc kép
    text = re.sub(r"“\s+", "“", text)
    text = re.sub(r"\s+”", "”", text)

    return text