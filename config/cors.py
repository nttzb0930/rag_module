import os

DEFAULT_CORS_ALLOWED_ORIGINS = (
    "http://localhost:5173,"
    "http://127.0.0.1:5173,"
    "http://localhost:5174,"
    "http://127.0.0.1:5174"
)

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        DEFAULT_CORS_ALLOWED_ORIGINS,
    ).split(",")
    if origin.strip()
]

CORS_ALLOW_ORIGIN_REGEX = r"https?://(localhost|127\.0\.0\.1):\d+"
