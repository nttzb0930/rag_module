import re

def extract_answers_from_output(llm_output: str, num_questions: int) -> dict:
        """
        Parse tất cả answers từ LLM output theo format [1]...[2]...
        Return dict {idx: answer} với idx là số thứ tự (1-based)
        """
        print(f"[DEBUG] LLM Output:\n{llm_output}\n") 
        # clean output
        pattern = r"Câu trả lời:\s*\n(.*)"
        match = re.search(pattern, llm_output, flags=re.DOTALL)
        if match:
            llm_output = match.group(1).strip()
        results = {}

        # Câu đơn return luôn
        if num_questions == 1:
            results[1] = llm_output.strip()
            return results
        # Câu có sub questions parse theo format [1] [2]
        for i in range(1, num_questions + 1):
            pattern = (
                rf"\[{i}\]\s.*?\n"
                r"(.*?)"
                rf"(?=\n\[{i+1}\]\s|\Z)"
            )
            m = re.search(pattern, llm_output, flags=re.DOTALL | re.IGNORECASE)
            if m:
                results[i] = m.group(1).strip()
        return results



def build_final_answer(sub_questions: list, final_map: dict) -> str:
    """
    Format final answer từ final_map
    """
    final_parts = []
    for i, sq in enumerate(sub_questions, start=1):
        ans = final_map.get(sq)
        if ans:
            final_parts.append(f"[{i}] Trích nguyên văn cho ý: {sq}\n{ans}")
        else:
            final_parts.append(f"[{i}] {sq}\n(Chưa có câu trả lời)")
    
    return "\n\n".join(final_parts)
