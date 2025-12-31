import re



# Split Summary Objective
def extract_summary_objective(full_text: str) -> list[str]:
    summary_section_pattern = r'MỤC\s+ĐÍCH\s+CỦA\s+CHƯƠNG\b.*?(?=\n\s*NỘI\s+DUNG\s+BÀI\s+GIẢNG\b|\n\s*CHƯƠNG\s+\d+:|\Z)'
    summary_objective = []
    # Tìm trong full_text với pattern - re.DOTALL để lấy cả xuống dòng - match.group() trả về chuỗi khớp - split() tách chuỗi theo bất kì khoảng trắng nào và bỏ qua các khoảng trắng rỗng
    # sau đó được nối lại với ' '.join() để thành chuỗi liền mạch & append vào list summary_section
    for match in re.finditer(summary_section_pattern, full_text, re.DOTALL):
        summary_objective.append(' '.join(match.group().split()))
    # trường hợp này đang làm với 1 chapter lên sẽ là vị trí đầu tiên trong list
    #summary_section = summary_section[0] if summary_section else "Không tìm thấy mục tiêu chương."
    return summary_objective