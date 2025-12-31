import re


# Split Detail Content
def extract_detail_content(full_text: str) -> list[str]:
    detail_content_pattern = r'NỘI\s+DUNG\s+BÀI\s+GIẢNG\b.*?(?=\n\s*NỘI\s+DUNG\s+ÔN\s+TẬP\s+VÀ\s+THẢO\s+LUẬN\b|\n\s*CHƯƠNG\s+\d+:|\Z)'
    detail_contents= []
    for match in re.finditer(detail_content_pattern, full_text, re.DOTALL):
        # detail_content = ' '.join(match.group().split()) (mất định dạng)
        detail_contents.append(re.sub(r'[ \t]+', ' ', match.group()).strip())
    return detail_contents