KTCT_KEYWORDS = [
    "hàng hóa",
    "thị trường",
    "giá trị",
    "lao động",
    "cung cầu",
    "tiền tệ",
    "dịch vụ",
    "cổ phiếu",
    "trái phiếu",
    "kinh tế thị trường",
]

LSD_KEYWORDS = [
    "cách mạng",
    "đảng cộng sản",
    "hồ chí minh",
    "kháng chiến",
    "giành chính quyền",
    "đại hội",
    "miền bắc",
    "miền nam",
    "chống mỹ",
    "đổi mới",
]

TRIET_KEYWORD = [
  "vật chất",
  "ý thức",
  "tồn tại xã hội",
  "ý thức xã hội",
  "mối liên hệ phổ biến",
  "sự phát triển",
  "phủ định biện chứng",
  "lượng",
  "chất",
  "điểm nút",
  "bước nhảy",
  "mâu thuẫn",
  "đấu tranh của các mặt đối lập",

  "nguyên nhân",
  "kết quả",
  "tất nhiên",
  "ngẫu nhiên",
  "nội dung",
  "hình thức",
  "bản chất",
  "hiện tượng",
  "khả năng",
  "hiện thực",

  "nhận thức",
  "thực tiễn",
  "nhận thức cảm tính",
  "nhận thức lý tính",
  "chân lý",
  "chân lý khách quan",
  "chân lý tuyệt đối",
  "chân lý tương đối",
  "tiêu chuẩn của chân lý",
  "sai lầm",

  "lực lượng sản xuất",
  "quan hệ sản xuất",
  "phương thức sản xuất",
  "cơ sở hạ tầng",
  "kiến trúc thượng tầng",
  "hình thái kinh tế xã hội",
  "đấu tranh giai cấp",
  "giai cấp",
  "nhà nước",
  "cách mạng xã hội",

  "con người",
  "bản chất con người",
  "lao động",
  "tha hóa",
  "tự do",
  "vai trò quần chúng nhân dân",
  "vai trò cá nhân",
  "lợi ích",
  "động lực phát triển xã hội",

  "ý thức chính trị",
  "ý thức pháp quyền",
  "ý thức đạo đức",
  "ý thức tôn giáo",
  "ý thức nghệ thuật",
  "ý thức khoa học",
  "tính độc lập tương đối của ý thức xã hội",

  "chủ nghĩa duy vật",
  "chủ nghĩa duy tâm",
  "chủ nghĩa siêu hình",
  "phép biện chứng",
  "chủ nghĩa duy vật biện chứng",
  "chủ nghĩa duy vật lịch sử",
  "học thuyết hình thái kinh tế xã hội",
  "quy luật giá trị",
  "chủ nghĩa xã hội khoa học"
]

def route_doc(question: str) -> str:
    """
    Router chọn corpus
    Nếu không match rõ ràng thì mặc định 'lsd'.
    """
    q = question.lower()

    if any(k in q for k in KTCT_KEYWORDS):
        return "ktct"
    if any(k in q for k in LSD_KEYWORDS):
        return "lsd"
    if any(k in q for k in TRIET_KEYWORD):
        return "triet"
    return None
