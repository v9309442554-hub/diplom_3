"""Test data and expected texts shared by the UI tests."""

from __future__ import annotations

# Ingredient details modal
INGREDIENT_MODAL_TITLE = "Детали ингредиента"
INGREDIENT_MODAL_STATS_COUNT = 4


class Messages:
    """Assertion messages shown in the test report."""

    CONSTRUCTOR_NOT_OPENED = "Конструктор не открылся"
    CONSTRUCTOR_NOT_OPENED_AFTER_CLICK = "Конструктор не открылся после клика на «Конструктор»"
    FEED_NOT_OPENED = "Лента заказов не открылась"
    FEED_NOT_OPENED_AFTER_CLICK = "Лента заказов не открылась после клика на «Лента заказов»"
    INGREDIENT_MODAL_NOT_OPENED = "Модальное окно с деталями ингредиента не открылось"
    INGREDIENT_MODAL_NOT_CLOSED = "Модальное окно не закрылось после клика по крестику"
    INGREDIENT_STATS_MISSING = "В окне должны быть пищевая ценность ингредиента"
    INGREDIENT_COUNTER_NOT_INCREASED = (
        "Счётчик ингредиента не увеличился: было {before}, стало {after}"
    )
    ORDER_NOT_IN_PROGRESS = "Заказа {order_number} нет в разделе «В работе»"
