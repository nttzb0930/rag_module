import re


# Split Chapter Title
def extract_chapter_title(full_text: str, chapter_pattern: str) -> list[str]:
    chapter_titles = []
    for match in re.finditer(chapter_pattern, full_text, re.DOTALL):
        chapter_titles.append(' '.join(match.group().split()))
    #chapter_title = chapter_titles[0] if chapter_titles else "Không tìm thấy tên chương."
    return chapter_titles