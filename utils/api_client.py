"""Minimal API client used to prepare and clean up test users."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.config import BASE_URL

REQUEST_TIMEOUT = 60
RETRY_ATTEMPTS = 3


@dataclass(frozen=True)
class User:
    email: str
    password: str
    name: str
    access_token: str = field(repr=False, default="")


class StellarBurgersAPI:
    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        retries = Retry(
            total=RETRY_ATTEMPTS,
            connect=RETRY_ATTEMPTS,
            read=RETRY_ATTEMPTS,
            status=RETRY_ATTEMPTS,
            backoff_factor=1,
            status_forcelist=(500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "POST", "DELETE"}),
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.mount("http://", HTTPAdapter(max_retries=retries))

    def register_user(self) -> User:
        email = f"ui_test_{uuid.uuid4().hex}@test.ru"
        response = self.session.post(
            f"{self.base_url}/api/auth/register",
            json={"email": email, "password": "Password123", "name": "UI Test"},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        if not payload.get("success"):
            raise RuntimeError(f"User registration failed: {payload}")
        return User(
            email=email,
            password="Password123",
            name="UI Test",
            access_token=payload["accessToken"],
        )

    def delete_user(self, access_token: str) -> None:
        response = self.session.delete(
            f"{self.base_url}/api/auth/user",
            headers={"Authorization": access_token},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        if not response.json().get("success"):
            raise RuntimeError(f"User deletion failed: {response.text}")
