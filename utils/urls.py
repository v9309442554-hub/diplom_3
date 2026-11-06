"""Page paths and helpers to build absolute URLs for the current stand."""

from __future__ import annotations

from utils.config import BASE_URL

CONSTRUCTOR_PATH = "/"
LOGIN_PATH = "/login"
ORDER_FEED_PATH = "/feed"


def url(path: str) -> str:
    """Build an absolute URL for a page path using the configured base address."""
    normalized = path if path.startswith("/") else f"/{path}"
    return f"{BASE_URL}{normalized}"
