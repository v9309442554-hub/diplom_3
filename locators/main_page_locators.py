from selenium.webdriver.common.by import By


class MainPageLocators:
    CONSTRUCTOR_LINK = (By.XPATH, "//a[contains(normalize-space(), 'Конструктор')]")
    ORDER_FEED_LINK = (By.XPATH, "//a[contains(normalize-space(), 'Лента')]")

    CONSTRUCTOR_HEADING = (By.XPATH, "//h1[normalize-space()='Соберите бургер']")

    INGREDIENT_CARDS = (By.CSS_SELECTOR, "a[href^='/ingredient/']")
    INGREDIENT_NAME = (By.CSS_SELECTOR, "p[class*='BurgerIngredient_ingredient__text']")
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "[class*='counter_counter__num']")

    BASKET = (By.CSS_SELECTOR, "section[class*='BurgerConstructor_basket'] ul")
    ORDER_BUTTON = (By.XPATH, "//button[contains(normalize-space(), 'Оформить заказ')]")

    MODAL_OPENED = (By.CSS_SELECTOR, "section[class*='Modal_modal_opened']")
    MODAL_TITLE = (By.CSS_SELECTOR, "section[class*='Modal_modal_opened'] [class*='Modal_modal__title__']")
    MODAL_CLOSE = (By.CSS_SELECTOR, "section[class*='Modal_modal_opened'] button[class*='Modal_modal__close']")
    MODAL_INGREDIENT_NAME = (
        By.CSS_SELECTOR,
        "section[class*='Modal_modal_opened'] p[class*='text_type_main-medium']",
    )
    MODAL_STATS = (By.CSS_SELECTOR, "section[class*='Modal_modal_opened'] ul[class*='statsList'] li")
