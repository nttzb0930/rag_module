import re
def fix_heading_broken_lines(text):
    lines = text.split("\n")
    fixed = []
    buffer = ""

    for line in lines:
        l = line.strip()

        # Nếu là heading thật
        if re.match(r'^\d+\.\d+(?:\.\d+)*\.', l):
            if buffer:
                fixed.append(buffer.strip())
                buffer = ""
            buffer = l
            continue

        # ULE GHÉP NĂM (1986-1996)
        if buffer and re.fullmatch(r'\d{4}\s*[-–]\s*\d{4}', l):
            buffer += f" ({l})"
            continue

        # RULE GHÉP TITLE BÌNH THƯỜNG
        if buffer and \
           re.match(r'^[a-zà-ỹ]', l) and \
           not re.match(r'^[-•+]\s', l) and \
           not re.match(r'^\d+\.\d+(?:\.\d+)*\.', l):

            buffer += " " + l
            continue

        # flush
        if buffer:
            fixed.append(buffer.strip())
            buffer = ""

        fixed.append(l)

    if buffer:
        fixed.append(buffer.strip())

    return "\n".join(fixed)
