# constants.py - Hằng số toàn ứng dụng

DATABASE_NAME = "smarttravel.db"

# Validation Rules
USERNAME_MIN_LENGTH = 3
PASSWORD_MIN_LENGTH = 6

# UI Configuration
PAGE_TITLE = "SmartTravel"
PAGE_LAYOUT = "wide"
NAV_ORIENTATION = "horizontal"

# CSS Colors
PRIMARY_COLOR = "#1877F2"
BACKGROUND_COLOR = "#F0F2F5"

# Database Tables
DB_TABLES = {
    "users": "users",
    "search_history": "search_history",
    "collections": "collections",
    "saved_places": "saved_places"
}

# Error Messages
ERROR_INVALID_USERNAME = "Tên đăng nhập phải có ít nhất {} ký tự."
ERROR_INVALID_PASSWORD = "Mật khẩu phải có ít nhất {} ký tự."
ERROR_PASSWORD_MISMATCH = "Mật khẩu xác nhận không khớp."
ERROR_LOGIN_FAILED = "Sai mật khẩu."
ERROR_USER_NOT_FOUND = "Tên đăng nhập không tồn tại."
ERROR_USER_EXISTS = "Tên đăng nhập đã tồn tại."
ERROR_DB_ERROR = "Lỗi cơ sở dữ liệu: {}"

# Success Messages
SUCCESS_LOGIN = "Đăng nhập thành công!"
SUCCESS_REGISTER = "Đăng ký thành công! Vui lòng đăng nhập."
SUCCESS_SAVED = "Đã lưu {}"

# File Types
ALLOWED_IMAGE_TYPES = ['jpg', 'png', 'jpeg']

# API Endpoints (TODO: Cấu hình khi có backend)
API_BASE_URL = "http://localhost:8000/api"
API_SEARCH_ENDPOINT = "/search"
API_RECOMMEND_ENDPOINT = "/recommend"
API_ANALYZE_ENDPOINT = "/analyze"
