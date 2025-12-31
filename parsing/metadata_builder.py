# Buid Metadata
def build_metadata(items, source: str):

    lookup = {item["number"]: item["title"] for item in items}

    for item in items:
        # phân cấp 
        number = item["number"]
        parts = number.split(".")
        level = len(parts)

        # 1) Parent
        parent = ".".join(parts[:-1]) if level > 2 else None

        # 2) Chapter root = 2 segments đầu
        if len(parts) >= 2:
            chapter_root = ".".join(parts[:2])
        else:
            chapter_root = number

        # 3) Path
        path = [".".join(parts[:i]) for i in range(1, len(parts) + 1)]

        # 4) Titles
        section_title = lookup.get(parent)
        chapter_title = lookup.get(chapter_root)

        # 5) Update
        item["parent"] = parent
        item["root"] = chapter_root
        item["path"] = path
        item["section_title"] = section_title
        item["chapter_title"] = chapter_title
        item["source"] = source
        item["content_length"] = len(item.get("content", ""))

    return items