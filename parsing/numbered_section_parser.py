import re

# Tách Theo Section
def extract_numbered_section(text):
    pattern = re.compile(r'^(\d+(?:\.\d+)+)\.\s+(.+?)\n(.*?)(?=^\d+(?:\.\d+)+\.\s|\Z)',re.DOTALL | re.MULTILINE)
    sections = []
    for m in pattern.finditer(text):
        num = m.group(1).strip()
        title = m.group(2).strip()
        content = m.group(3).strip()

        # FIX: nếu title chứa "*", tách title đúng chuẩn
        if " * " in title:
            parts = title.split(" * ", 1)
            title = parts[0].strip()
            content = "* " + parts[1].strip() + "\n" + content

        sections.append({
            "number": num,
            "title": title,
            "content": content,
            "level": num.count(".")
        })

    return sections
\\