import re
# Từ docs đã build metadata thấy content còn dài > 10k, lọc lại content thấy (*) vẫn còn chia được nhỏ tiếp, tiếp tục chia nhỏ
def extract_star_bullets(text, parent_path):
    bullets = []
    counter = 1

    matches = list(re.finditer(r'^\s*\*\s+(.*)$', text, flags=re.MULTILINE))

    for i, m in enumerate(matches):
        start_block = m.start()
        if i + 1 < len(matches):
            end_block = matches[i + 1].start()
        else:
            end_block = len(text)

        block = text[start_block:end_block].strip()
        lines = block.splitlines()
        if not lines:
            continue

        first_line = lines[0].strip()
        first_line = re.sub(r'^\s*\*\s+', '', first_line)

        if ":" in first_line:
            raw_title, first_rest = first_line.split(":", 1)
            bullet_title = raw_title.strip()
            first_content_part = first_rest.strip()
        else:
            bullet_title = first_line.strip()
            first_content_part = ""

        other_lines = [l.strip() for l in lines[1:] if l.strip()]

        content_parts = []
        if first_content_part:
            content_parts.append(first_content_part)
        if other_lines:
            content_parts.append("\n".join(other_lines))

        bullet_content = "\n".join(content_parts).strip()

        bullets.append({
            "bullet_index": counter,
            "bullet_title": bullet_title,
            "bullet_content": bullet_content,
            "path": parent_path.copy(),
            "start": start_block,
            "end": end_block
        })

        counter += 1

    return bullets
