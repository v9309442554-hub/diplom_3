"""UI tests for the order feed."""

from __future__ import annotations

import allure

from pages.feed_page import FeedPage
from pages.main_page import MainPage
from utils.api_client import User


@allure.epic("Stellar Burgers")
@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.story("Счётчики выполненных заказов")
    @allure.title("Счётчик «Выполнено за всё время» увеличивается после создания заказа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_total_completed_counter_increases(
        self, authorized_user: User, main_page: MainPage, feed_page: FeedPage
    ) -> None:
        feed_page.open()
        total_before = feed_page.get_total_completed()

        main_page.open()
        main_page.create_order()

        feed_page.open()
        feed_page.wait_for_total_completed_greater_than(total_before)

        assert feed_page.get_total_completed() > total_before

    @allure.story("Счётчики выполненных заказов")
    @allure.title("Счётчик «Выполнено за сегодня» увеличивается после создания заказа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_today_completed_counter_increases(
        self, authorized_user: User, main_page: MainPage, feed_page: FeedPage
    ) -> None:
        feed_page.open()
        today_before = feed_page.get_today_completed()

        main_page.open()
        main_page.create_order()

        feed_page.open()
        feed_page.wait_for_today_completed_greater_than(today_before)

        assert feed_page.get_today_completed() > today_before

    @allure.story("Заказы в работе")
    @allure.title("Номер нового заказа появляется в разделе «В работе»")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_new_order_number_appears_in_progress(
        self, authorized_user: User, main_page: MainPage, feed_page: FeedPage
    ) -> None:
        main_page.open()
        order_number = main_page.create_order()

        feed_page.open()
        feed_page.wait_for_order_in_progress(order_number)

        in_progress_numbers = {str(int(number)) for number in feed_page.get_in_progress_numbers()}
        assert str(int(order_number)) in in_progress_numbers, (
            f"Заказа {order_number} нет в разделе «В работе»"
        )
