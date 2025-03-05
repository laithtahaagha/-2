import os

# Database configuration
DB_PATH = os.path.join(os.path.expanduser('~'), 'ArchiveSystem', 'data.db')

# Application settings
APP_NAME = "نظام الأرشفة للدراسات العليا"
APP_VERSION = "1.0.0"
AUTHOR = "Laith Agha"

# Default theme
DEFAULT_THEME = "light"

# Supported languages
LANGUAGES = {
    "ar": "العربية",
    "en": "English"
}

# File upload settings
ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Scanner settings
SCANNER_DPI = 300
SCANNER_COLOR_MODE = 'RGB'
