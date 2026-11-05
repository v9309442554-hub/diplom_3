"""Page object for the burger constructor (main page)."""

from __future__ import annotations

import allure

from locators.main_page_locators import MainPageLocators as Locators
from pages.base_page import BasePage
from utils.config import LONG_TIMEOUT


class MainPage(BasePage):
    path = "/"

    @allure.step("Открыть конструктор")
    def open(self) -> "MainPage":
        super().open()
        return self

    def is_opened(self) -> bool:
        return self.is_visible(Locators.CONSTRUCTOR_HEADING)

    @allure.step("Перейти в конструктор по ссылке в шапке")
    def go_to_constructor(self) -> None:
        self.click(Locators.CONSTRUCTOR_LINK)

    @allure.step("Перейти в ленту заказов по ссылке в шапке")
    def go_to_order_feed(self) -> None:
        self.click(Locators.ORDER_FEED_LINK)

    def get_ingredient_cards(self):
        return self.find_all(Locators.INGREDIENT_CARDS)

    def get_ingredient_name(self, index: int = 0) -> str:
        card = self.get_ingredient_cards()[index]
        return card.find_element(*Locators.INGREDIENT_NAME).text.strip()

    def get_ingredient_counter(self, index: int = 0) -> int:
        card = self.get_ingredient_cards()[index]
        return int(card.find_element(*Locators.INGREDIENT_COUNTER).text.strip())

    @allure.step("Открыть детали ингредиента №{index}")
    def open_ingredient_details(self, index: int = 0) -> str:
        card = self.get_ingredient_cards()[index]
        ingredient_name = card.find_element(*Locators.INGREDIENT_NAME).text.strip()
        self.scroll_to(card)
        card.click()
        self.find(Locators.MODAL_OPENED)
        return ingredient_name

    def is_modal_opened(self) -> bool:
        return any(
            "Modal_modal_opened" in (element.get_attribute("class") or "")
            and element.is_displayed()
            for element in self.elements(Locators.MODAL_OPENED)
        )

    def get_modal_title(self) -> str:
        return self.find(Locators.MODAL_TITLE).text.strip()

    def get_modal_ingredient_name(self) -> str:
        return self.find(Locators.MODAL_INGREDIENT_NAME).text.strip()

    def get_modal_stats(self) -> list[str]:
        return [element.text.strip() for element in self.elements(Locators.MODAL_STATS)]

    @allure.step("Закрыть модальное окно крестиком")
    def close_modal(self) -> None:
        self.click(Locators.MODAL_CLOSE)
        self.wait_until(
            lambda _: not self.is_modal_opened(),
            message="Модальное окно не закрылось",
        )

    @allure.step("Добавить ингредиент №{index} в заказ")
    def add_ingredient_to_basket(self, index: int = 0) -> None:
        card = self.get_ingredient_cards()[index]
        counter_before = self.get_ingredient_counter(index)
        basket = self.find(Locators.BASKET)
        self.drag_and_drop(card, basket)
        self.wait_until(
            lambda _: self.get_ingredient_counter(index) > counter_before,
            message="Счётчик ингредиента не увеличился после добавления в заказ",
        )

    @allure.step("Дождаться появления номера заказа")
    def get_order_number(self) -> str:
        self.wait_until(
            lambda _: self.get_modal_title().isdigit(),
            timeout=LONG_TIMEOUT,
            message="Номер заказа не появился в модальном окне",
        )
        return self.get_modal_title()

    @allure.step("Оформить заказ")
    def create_order(self) -> str:
        self.add_ingredient_to_basket(0)
        self.click(Locators.ORDER_BUTTON)
        order_number = self.get_order_number()
        self.close_modal()
        return order_number
