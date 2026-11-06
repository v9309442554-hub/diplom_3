"""Page object for the login page."""

from __future__ import annotations

import allure

from locators.login_page_locators import LoginPageLocators as Locators
from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    @allure.step("Открыть страницу входа")
    def open(self) -> "LoginPage":
        super().open()
        return self

    @allure.step("Войти в аккаунт пользователя {email}")
    def login(self, email: str, password: str) -> None:
        self.open()
        self.find(Locators.EMAIL_INPUT).send_keys(email)
        self.find(Locators.PASSWORD_INPUT).send_keys(password)
        self.click(Locators.LOGIN_BUTTON)
        self.wait_for_url_path("/")
