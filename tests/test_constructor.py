"""UI tests for the burger constructor."""

from __future__ import annotations

import allure

from pages.feed_page import FeedPage
from pages.main_page import MainPage


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
        assert feed_page.is_opened(), "Лента заказов не открылась"

        main_page.go_to_constructor()

        main_page.wait_for_url_path("/")
        assert main_page.is_opened(), "Конструктор не открылся после клика на «Конструктор»"

    @allure.story("Навигация")
    @allure.title("Переход в ленту заказов по клику на «Лента заказов»")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_feed_link_navigates_to_order_feed(
        self, main_page: MainPage, feed_page: FeedPage
    ) -> None:
        main_page.open()
        assert main_page.is_opened(), "Конструктор не открылся"

        main_page.go_to_order_feed()

        feed_page.wait_for_url_path("/feed")
        assert feed_page.is_opened(), "Лента заказов не открылась после клика на «Лента заказов»"

    @allure.story("Детали ингредиента")
    @allure.title("При клике на ингредиент открывается всплывающее окно с деталями")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ingredient_details_modal_opens(self, main_page: MainPage) -> None:
        main_page.open()
        ingredient_name = main_page.open_ingredient_details(0)

        assert main_page.is_modal_opened(), "Модальное окно с деталями ингредиента не открылось"
        assert main_page.get_modal_title() == "Детали ингредиента"
        assert ingredient_name in main_page.get_modal_ingredient_name()
        assert len(main_page.get_modal_stats()) == 4, "В окне должны быть пищевая ценность ингредиента"

    @allure.story("Детали ингредиента")
    @allure.title("Всплывающее окно с деталями закрывается кликом по крестику")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ingredient_details_modal_closes_by_cross(self, main_page: MainPage) -> None:
        main_page.open()
        main_page.open_ingredient_details(0)
        assert main_page.is_modal_opened(), "Модальное окно не открылось"

        main_page.close_modal()

        assert not main_page.is_modal_opened(), "Модальное окно не закрылось после клика по крестику"

    @allure.story("Счётчики ингредиентов")
    @allure.title("Счётчик ингредиента увеличивается при добавлении в заказ")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ingredient_counter_increases_when_added_to_order(self, main_page: MainPage) -> None:
        main_page.open()
        counter_before = main_page.get_ingredient_counter(0)

        main_page.add_ingredient_to_basket(0)

        counter_after = main_page.get_ingredient_counter(0)
        assert counter_after > counter_before, (
            f"Счётчик ингредиента не увеличился: было {counter_before}, стало {counter_after}"
        )
