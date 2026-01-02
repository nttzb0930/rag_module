from rag_module.config import NO_SPLIT_SECTION_PATH_LSD
import re
# từ docs đã build metadata thấy content còn dài > 10k, lọc lại content thấy (*) vẫn còn chia được nhỏ tiếp, tiếp tục chia nhỏ
def extract_star_bullets(text, parent_path, section_path=None):
    """
    text: detail content sau khi đã được clean và fix heading
    parent_path:
    section_path: lọc section không bắt bullet
    """
    # loại các section khó bắt theo bullet
    if section_path and section_path in NO_SPLIT_SECTION_PATH_LSD:
        return []
    

    bullets = []
    counter = 1
    # lưu lại line + offset để tra dòng trước
    lines = text.splitlines()
    line_starts = []
    pos = 0
    for ln in lines:
        line_starts.append(pos)
        pos += len(ln) + 1  # +1 vì splitlines() bỏ \n
    matches = list(re.finditer(r'^\s*\*\s+(.*)$', text, flags=re.MULTILINE))
    if not matches:
        return bullets
    def is_new_bullet(match_start):
        # tìm line index của match
        line_idx = 0
        for i, s in enumerate(line_starts):
            if s <= match_start:
                line_idx = i

        # text của dòng hiện tại (sau dấu *)
        cur_line = lines[line_idx].strip()
        cur_text = re.sub(r'^\s*\*\s+', '', cur_line)
        # RULE: nếu dòng kết thúc bằng dấu câu -> không tách bullet mới
        if cur_text.rstrip().endswith((':', '.', ';', ',', '…')):
            return False
        # tìm dòng kế tiếp có text 
        k = line_idx + 1
        while k < len(lines) and not lines[k].strip():
            k += 1
        next_line = lines[k].strip() if k < len(lines) else ""
        # nếu dạng "Label:" và dòng sau bắt đầu bằng "-" / "•" / "+"
        if cur_text.endswith(":") and re.match(r'^[-•+]\s', next_line):
            return True
        # nếu có ":" nhưng không có list con => coi là content
        if ":" in cur_text and not re.match(r'^[-•+]\s', next_line):
            return False
        # giữ logic cũ
        j = line_idx - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        if j < 0:
            return True
        prev = lines[j].strip()
        if prev.startswith("*"):
            return False
        if prev.startswith("*") and prev.endswith(":"):
            return False
        return True

    filtered = []
    for m in matches:
        if not is_new_bullet(m.start()):
            continue
        filtered.append(m)
    # dùng filtered thay vì matches trong phần xử lý tiếp theo
    for i, m in enumerate(filtered):
        start_block = m.start()
        if i + 1 < len(filtered):
            end_block = filtered[i + 1].start()
        else:
            end_block = len(text)

        block = text[start_block:end_block].strip()
        block_lines  = block.splitlines()
        if not block_lines:
            continue

        first_line = block_lines[0].strip()
        first_line = re.sub(r'^\s*\*\s+', '', first_line)

        if ":" in first_line:
            raw_title, first_rest = first_line.split(":", 1)
            bullet_title = raw_title.strip()
            first_content_part = first_rest.strip()
            if len(first_content_part) > 300:
                # không coi Ý nghĩa Luận cương chính trị tháng 10/1930: Luận cương đã ... là bullet (1.2.1.2)
                continue
        else:
            bullet_title = first_line.strip()
            first_content_part = ""

        other_lines = [l.strip() for l in block_lines[1:] if l.strip()]

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
