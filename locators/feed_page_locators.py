from selenium.webdriver.common.by import By


class FeedPageLocators:
    FEED_HEADING = (By.XPATH, "//h1[contains(normalize-space(), 'Лента заказов')]")

    TOTAL_COMPLETED_COUNTER = (
        By.XPATH,
        "//p[contains(normalize-space(), 'Выполнено за все время')]"
        "/following-sibling::p[contains(@class, 'OrderFeed_number')]",
    )
    TODAY_COMPLETED_COUNTER = (
        By.XPATH,
        "//p[contains(normalize-space(), 'Выполнено за сегодня')]"
        "/following-sibling::p[contains(@class, 'OrderFeed_number')]",
    )

    IN_PROGRESS_ITEMS = (By.CSS_SELECTOR, "ul[class*='OrderFeed_orderListReady'] li")
