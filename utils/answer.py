import re


def clean_answer_text(answer: str) -> str:
    """
    Dọn dẹp các wrapper định dạng như "[1] Trích nguyên văn..."
    nhưng giữ nguyên nội dung trích dẫn.
    """
    text = (answer or "").strip()
    text = re.sub(r"^Câu trả lời:\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(
        r"^\[\d+\]\s*Trích nguyên văn cho ý:.*?\n+",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(r"^-\s*\[\d+\]\s*", "- ", text)
    return text.strip()


def extract_answers_from_output(llm_output: str, num_questions: int) -> dict:
    """
    Parse tất cả answers từ LLM output theo format [1]...[2]...
    Return dict {idx: answer} với idx là số thứ tự (1-based)
    """
    print(f"[DEBUG] LLM Output:\n{llm_output}\n")

    pattern = r"Câu trả lời:\s*\n(.*)"
    match = re.search(pattern, llm_output, flags=re.DOTALL)
    if match:
        llm_output = match.group(1).strip()

    results = {}

    if num_questions == 1:
        results[1] = clean_answer_text(llm_output)
        return results

    for i in range(1, num_questions + 1):
        pattern = (
            rf"\[{i}\]\s.*?\n"
            r"(.*?)"
            rf"(?=\s*\[{i+1}\]\s|\Z)"
        )
        m = re.search(pattern, llm_output, flags=re.DOTALL | re.IGNORECASE)
        if m:
            results[i] = clean_answer_text(m.group(1))
    return results


def build_final_answer(sub_questions: list, final_map: dict) -> str:
    """
    Format final answer từ final_map
    """
    if len(sub_questions) == 1:
        ans = clean_answer_text(final_map.get(sub_questions[0], ""))
        return ans if ans else "(Chưa có câu trả lời)"

    final_parts = []
    for i, sq in enumerate(sub_questions, start=1):
        ans = clean_answer_text(final_map.get(sq, ""))
        if ans:
            final_parts.append(f"{i}. {sq}\n{ans}")
        else:
            final_parts.append(f"{i}. {sq}\n(Chưa có câu trả lời)")

    return "\n\n".join(final_parts)
