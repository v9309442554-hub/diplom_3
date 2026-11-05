"""Project configuration loaded from environment variables."""

import os

BASE_URL = os.getenv("BASE_URL", "https://stellarburgers.education-services.ru").rstrip("/")
HEADLESS = os.getenv("HEADLESS", "true").strip().lower() not in {"0", "false", "no"}

DEFAULT_TIMEOUT = float(os.getenv("DEFAULT_TIMEOUT", "10"))
LONG_TIMEOUT = float(os.getenv("LONG_TIMEOUT", "30"))

WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))
