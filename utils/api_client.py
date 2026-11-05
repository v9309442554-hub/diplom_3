"""Minimal API client used to prepare test users."""

from __future__ import annotations

import uuid
from dataclasses import dataclass

import requests

from utils.config import BASE_URL


@dataclass(frozen=True)
class User:
    email: str
    password: str
    name: str


class StellarBurgersAPI:
    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def register_user(self) -> User:
        user = User(
            email=f"ui_test_{uuid.uuid4().hex}@test.ru",
            password="Password123",
            name="UI Test",
        )
        response = self.session.post(
            f"{self.base_url}/api/auth/register",
            json={
                "email": user.email,
                "password": user.password,
                "name": user.name,
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        if not payload.get("success"):
            raise RuntimeError(f"User registration failed: {payload}")
        return user
