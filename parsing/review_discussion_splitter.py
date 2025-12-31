import re



# Split Review And Discussion
def extract_review_discussion(full_text: str) -> list[str]:
    review_discussion_pattern = r'NỘI\s+DUNG\s+ÔN\s+TẬP\s+VÀ\s+THẢO\s+LUẬN\b.*?(?=\n\s*CHƯƠNG\s+\d+:|\Z)'
    review_discussion_contents = []
    for match in re.finditer(review_discussion_pattern, full_text, re.DOTALL):
        review_discussion_contents.append(' '.join(match.group().split()))
    return review_discussion_contents