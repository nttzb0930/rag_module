import re



def fix_heading_broken_lines(text: str) -> str:
    """
    ERR:
        1.2.1.3. Cuộc đấu tranh khôi phục tổ chức và phong trào cách mạng, Đại hội 
        Đảng lần thứ I (tháng 3/1935)
    FIXED:         
        1.2.1.3. Cuộc đấu tranh khôi phục tổ chức và phong trào cách mạng, Đại hội Đảng lần thứ I (tháng 3/1935)
    """
    lines = text.split("\n")
    fixed = []
    buffer = ""

    for line in lines:
        l = line.strip()

        # Nếu là heading thật
        if re.match(r'^\d+\.\d+(?:\.\d+)*\.?', l):

            # đẩy heading cũ
            if buffer:
                fixed.append(buffer.strip())
                buffer = ""

            buffer = l  # bắt đầu heading mới
            continue
        # Rule ghép năm ()
        m = re.fullmatch(r'\(?\s*(\d{4})\s*[-–—‑−]\s*(\d{4})\s*\)?', l)
        if buffer and m:
            buffer += f" ({m.group(1)}-{m.group(2)})"
            continue
        # RULE GHÉP TITLE:
        # chỉ ghép vào TITLE khi dòng bắt đầu bằng CHỮ THƯỜNG và không phải bullet, không phải heading
        if buffer and \
           re.match(r'^[a-zà-ỹ]', l) and \
           not re.match(r'^[-•+]\s', l) and \
           not re.match(r'^\d+\.\d+(?:\.\d+)*\.?', l):

            buffer += " " + l
            continue

        # nếu không ghép được → flush title vào fixed
        if buffer:
            fixed.append(buffer.strip())
            buffer = ""

        fixed.append(l)

    if buffer:
        fixed.append(buffer.strip())

    return "\n".join(fixed)
