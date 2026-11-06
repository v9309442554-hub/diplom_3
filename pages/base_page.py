"""Base page object with common browser interactions."""

from __future__ import annotations

from urllib.parse import urlparse

import allure
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import DEFAULT_TIMEOUT
from utils.urls import url


class BasePage:
    path = "/"

    def __init__(self, driver: WebDriver, timeout: float = DEFAULT_TIMEOUT) -> None:
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открыть страницу {path}")
    def open(self, path: str | None = None) -> "BasePage":
        target = path or self.path
        if not target.startswith("/"):
            target = f"/{target}"
        self.driver.get(url(target))
        return self

    @allure.step("Найти элемент {locator}")
    def find(self, locator: tuple[str, str], timeout: float | None = None) -> WebElement:
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Найти все элементы {locator}")
    def find_all(self, locator: tuple[str, str], timeout: float | None = None) -> list[WebElement]:
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(lambda driver: driver.find_elements(*locator) or False)

    @allure.step("Получить элементы {locator}")
    def elements(self, locator: tuple[str, str]) -> list[WebElement]:
        return self.driver.find_elements(*locator)

    @allure.step("Кликнуть по элементу {locator}")
    def click(self, locator: tuple[str, str], timeout: float | None = None) -> None:
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementClickInterceptedException:
            # Firefox hit-tests hidden modal overlays, so fall back to a JS click.
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator: tuple[str, str]) -> str:
        return self.find(locator).text.strip()

    @allure.step("Проверить видимость элемента {locator}")
    def is_visible(self, locator: tuple[str, str], timeout: float = DEFAULT_TIMEOUT) -> bool:
        try:
            WebDriverWait(self.driver, max(timeout, 0.1)).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Дождаться выполнения условия")
    def wait_until(self, condition, timeout: float | None = None, message: str = ""):
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(condition, message=message)

    @allure.step("Дождаться URL с путём {path}")
    def wait_for_url_path(self, path: str, timeout: float | None = None) -> None:
        expected = path.rstrip("/")

        def path_matches(driver: WebDriver) -> bool:
            return urlparse(driver.current_url).path.rstrip("/") == expected

        self.wait_until(
            path_matches,
            timeout=timeout,
            message=f"Expected URL path '{path}', got '{urlparse(self.driver.current_url).path}'",
        )

    @allure.step("Проскроллить к элементу")
    def scroll_to(self, element: WebElement) -> None:
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element
        )

    @allure.step("Перетащить ингредиент в корзину")
    def drag_and_drop(self, source: WebElement, target: WebElement) -> None:
        """Dispatch native HTML5 drag-and-drop events.

        Selenium ActionChains does not trigger drag-and-drop in Firefox,
        so events are dispatched directly for consistent cross-browser behavior.
        """
        self.driver.execute_script(
            """
            const source = arguments[0];
            const target = arguments[1];
            const dataTransfer = new DataTransfer();
            const fire = (element, type) => element.dispatchEvent(
                new DragEvent(type, {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dataTransfer
                })
            );

            fire(source, 'dragstart');
            fire(target, 'dragenter');
            fire(target, 'dragover');
            fire(target, 'drop');
            fire(source, 'dragend');
            """,
            source,
            target,
        )
