"""Page object for the order feed."""

from __future__ import annotations

import re

import allure

from locators.feed_page_locators import FeedPageLocators as Locators
from pages.base_page import BasePage
from utils.config import LONG_TIMEOUT


class FeedPage(BasePage):
    path = "/feed"

    @allure.step("Открыть ленту заказов")
    def open(self) -> "FeedPage":
        super().open()
        return self

    def is_opened(self) -> bool:
        return self.is_visible(Locators.FEED_HEADING)

    def _get_counter(self, locator: tuple[str, str]) -> int:
        digits = re.sub(r"\D", "", self.get_text(locator))
        return int(digits)

    def get_total_completed(self) -> int:
        return self._get_counter(Locators.TOTAL_COMPLETED_COUNTER)

    def get_today_completed(self) -> int:
        return self._get_counter(Locators.TODAY_COMPLETED_COUNTER)

    def get_in_progress_numbers(self) -> list[str]:
        numbers = []
        for element in self.elements(Locators.IN_PROGRESS_ITEMS):
            text = element.text.strip()
            if text.isdigit():
                numbers.append(text)
        return numbers

    @allure.step("Дождаться увеличения счётчика «Выполнено за всё время»")
    def wait_for_total_completed_greater_than(self, value: int) -> None:
        self.wait_until(
            lambda _: self.get_total_completed() > value,
            timeout=LONG_TIMEOUT,
            message="Счётчик «Выполнено за всё время» не увеличился",
        )

    @allure.step("Дождаться увеличения счётчика «Выполнено за сегодня»")
    def wait_for_today_completed_greater_than(self, value: int) -> None:
        self.wait_until(
            lambda _: self.get_today_completed() > value,
            timeout=LONG_TIMEOUT,
            message="Счётчик «Выполнено за сегодня» не увеличился",
        )

    @allure.step("Дождаться появления заказа {order_number} в разделе «В работе»")
    def wait_for_order_in_progress(self, order_number: str) -> None:
        expected = str(int(order_number))

        def order_is_present(_) -> bool:
            numbers = {str(int(number)) for number in self.get_in_progress_numbers()}
            return expected in numbers

        self.wait_until(
            order_is_present,
            timeout=LONG_TIMEOUT,
            message=f"Заказ {order_number} не появился в разделе «В работе»",
        )
