"""UI tests for the burger constructor."""

from __future__ import annotations

import allure

from pages.feed_page import FeedPage
from pages.main_page import MainPage
from utils.test_data import INGREDIENT_MODAL_STATS_COUNT, INGREDIENT_MODAL_TITLE, Messages
from utils.urls import CONSTRUCTOR_PATH, ORDER_FEED_PATH


@allure.epic("Stellar Burgers")
@allure.feature("Конструктор")
class TestConstructor:
    @allure.story("Навигация")
    @allure.title("Переход в конструктор по клику на «Конструктор»")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_constructor_link_navigates_to_constructor(
        self, main_page: MainPage, feed_page: FeedPage
    ) -> None:
        feed_page.open()
        assert feed_page.is_opened(), Messages.FEED_NOT_OPENED

        main_page.go_to_constructor()

        main_page.wait_for_url_path(CONSTRUCTOR_PATH)
        assert main_page.is_opened(), Messages.CONSTRUCTOR_NOT_OPENED_AFTER_CLICK

    @allure.story("Навигация")
    @allure.title("Переход в ленту заказов по клику на «Лента заказов»")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_feed_link_navigates_to_order_feed(
        self, opened_main_page: MainPage, feed_page: FeedPage
    ) -> None:
        assert opened_main_page.is_opened(), Messages.CONSTRUCTOR_NOT_OPENED

        opened_main_page.go_to_order_feed()

        feed_page.wait_for_url_path(ORDER_FEED_PATH)
        assert feed_page.is_opened(), Messages.FEED_NOT_OPENED_AFTER_CLICK

    @allure.story("Детали ингредиента")
    @allure.title("При клике на ингредиент открывается всплывающее окно с деталями")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ingredient_details_modal_opens(self, opened_main_page: MainPage) -> None:
        ingredient_name = opened_main_page.open_ingredient_details(0)

        assert opened_main_page.is_modal_opened(), Messages.INGREDIENT_MODAL_NOT_OPENED
        assert opened_main_page.get_modal_title() == INGREDIENT_MODAL_TITLE
        assert ingredient_name in opened_main_page.get_modal_ingredient_name()
        assert (
            len(opened_main_page.get_modal_stats()) == INGREDIENT_MODAL_STATS_COUNT
        ), Messages.INGREDIENT_STATS_MISSING

    @allure.story("Детали ингредиента")
    @allure.title("Всплывающее окно с деталями закрывается кликом по крестику")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ingredient_details_modal_closes_by_cross(self, opened_main_page: MainPage) -> None:
        opened_main_page.open_ingredient_details(0)
        assert opened_main_page.is_modal_opened(), Messages.INGREDIENT_MODAL_NOT_OPENED

        opened_main_page.close_modal()

        assert not opened_main_page.is_modal_opened(), Messages.INGREDIENT_MODAL_NOT_CLOSED

    @allure.story("Счётчики ингредиентов")
    @allure.title("Счётчик ингредиента увеличивается при добавлении в заказ")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ingredient_counter_increases_when_added_to_order(
        self, opened_main_page: MainPage
    ) -> None:
        counter_before = opened_main_page.get_ingredient_counter(0)

        opened_main_page.add_ingredient_to_basket(0)

        counter_after = opened_main_page.get_ingredient_counter(0)
        assert counter_after > counter_before, Messages.INGREDIENT_COUNTER_NOT_INCREASED.format(
            before=counter_before, after=counter_after
        )
