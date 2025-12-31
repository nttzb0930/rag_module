import re
def debug_all(combined_docs, ):
    print("\n================ DEBUG REPORT ================\n")

    # --------------------------------------------------
    # 1) Missing chapter_number
    # --------------------------------------------------
    missing_chap = [
        (i, d.metadata.get("type"), d.page_content[:80])
        for i, d in enumerate(combined_docs)
        if d.metadata.get("chapter_number") is None
    ]
    print("Missing chapter_number:", len(missing_chap))
    print(missing_chap[:5], "\n")


    # --------------------------------------------------
    # 2) Invalid heading number (parse section lỗi)
    # --------------------------------------------------
    invalid_heading = [
        (i, d.metadata.get("number"), d.page_content[:80])
        for i, d in enumerate(combined_docs)
        if d.metadata.get("number")
        and not re.fullmatch(r'\d+(\.\d+)*', d.metadata["number"])
    ]
    print("Invalid heading number:", len(invalid_heading))
    print(invalid_heading[:5], "\n")


    # --------------------------------------------------
    # 3) Bullet split errors (* còn sót)
    # --------------------------------------------------
    bullet_errors = [
        (i, d.page_content[:100])
        for i, d in enumerate(combined_docs)
        if d.metadata.get("type") == "bullet"
        and "*" in d.page_content[:5]
    ]
    print("Bullet split errors:", len(bullet_errors))
    print(bullet_errors[:5], "\n")


    # --------------------------------------------------
    # 4) Objective completeness (kiến thức - tư tưởng - kỹ năng)
    # --------------------------------------------------
    objective_check = {}
    for d in combined_docs:
        if d.metadata.get("type") == "objective":
            chap = d.metadata["chapter_number"]
            objective_check.setdefault(chap, set()).add(d.metadata["objective_type"])
    print("Objective coverage per chapter:")
    print(objective_check, "\n")


    # --------------------------------------------------
    # 5) PATH CHECK —
    # --------------------------------------------------
    missing_path = []
    real_path_errors = []

    for i, d in enumerate(combined_docs):
        if d.metadata.get("path") is None:
            missing_path.append((i, d.metadata.get("type"), d.page_content[:80]))

            # Chỉ count lỗi thật nếu type không phải objective
            if d.metadata.get("type") != "objective":
                real_path_errors.append((i, d.metadata.get("type"), d.page_content[:80]))

    print("Missing path (tổng):", len(missing_path))
    print(missing_path[:5], "\n")

    print("REAL path errors (bỏ qua objective):", len(real_path_errors))
    print(real_path_errors[:5], "\n")

    print("\n================ END DEBUG ================\n")