import os

DEFAULT_CORS_ALLOWED_ORIGINS = (
    "http://localhost:5174,"
    "http://127.0.0.1:5174,"
    "https://790f-2402-800-6d3e-645b-59ab-518a-b2a3-f12f.ngrok-free.app"
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
