"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import json
import os
import platform
from typing import Iterator

import allure
import pytest
from allure_commons.types import ParameterMode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.driver_finder import DriverFinder
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.remote_connection import FirefoxRemoteConnection
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver

from pages.feed_page import FeedPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from utils.api_client import StellarBurgersAPI, User
from utils.config import BASE_URL, HEADLESS, WINDOW_HEIGHT, WINDOW_WIDTH

BROWSERS = ("chrome", "firefox")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        action="store",
        default="all",
        choices=("all", *BROWSERS),
        help="Browser to run UI tests in (default: all).",
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browsers with a visible window.",
    )


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if "browser_name" in metafunc.fixturenames:
        selected = metafunc.config.getoption("--browser")
        browsers = list(BROWSERS) if selected == "all" else [selected]
        metafunc.parametrize(
            "browser_name",
            [pytest.param(browser, id=browser) for browser in browsers],
        )


@pytest.fixture
def browser_name(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture
def driver(browser_name: str, request: pytest.FixtureRequest):
    headless = HEADLESS and not request.config.getoption("--headed")
    browser, service = _start_browser(browser_name, headless)

    browser.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    browser.set_page_load_timeout(60)
    # Hide the raw pytest parameter and expose a readable one in Allure.
    allure.dynamic.parameter(
        "browser_name", browser_name, mode=ParameterMode.HIDDEN
    )
    allure.dynamic.parameter("Browser", browser_name)

    try:
        yield browser
    finally:
        browser.quit()
        if service is not None:
            service.stop()


def _start_browser(
    browser_name: str, headless: bool, attempts: int = 2
) -> tuple[WebDriver, FirefoxService | None]:
    """Start a browser, retrying once on intermittent WebDriver startup errors."""
    last_error: Exception | None = None

    for attempt in range(1, attempts + 1):
        try:
            if browser_name == "chrome":
                options = ChromeOptions()
                if headless:
                    options.add_argument("--headless=new")
                options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-notifications")
                options.add_argument("--lang=ru-RU")
                options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
                return webdriver.Chrome(options=options), None

            if browser_name == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("-headless")
                options.add_argument(f"--width={WINDOW_WIDTH}")
                options.add_argument(f"--height={WINDOW_HEIGHT}")
                options.set_preference("intl.accept_languages", "ru-RU")
                return _create_firefox_driver(options)

            raise pytest.UsageError(f"Unsupported browser: {browser_name}")
        except pytest.UsageError:
            raise
        except Exception as error:  # noqa: BLE001 - startup errors differ per browser
            last_error = error
            if attempt == attempts:
                break

    raise RuntimeError(f"Failed to start {browser_name}") from last_error


def _create_firefox_driver(options: FirefoxOptions) -> tuple[WebDriver, FirefoxService]:
    """Start Firefox through geckodriver reachable by IPv4.

    Selenium connects to ``localhost`` which may resolve to IPv6 (``::1``) first,
    while geckodriver listens on ``127.0.0.1`` only. That mismatch makes session
    creation hang until the 120 second connection timeout.
    """
    service = FirefoxService()
    service.path = DriverFinder(service, options).get_driver_path()
    service.start()

    executor = FirefoxRemoteConnection(
        remote_server_addr=service.service_url.replace("localhost", "127.0.0.1"),
        keep_alive=True,
    )
    try:
        browser = WebDriver(command_executor=executor, options=options)
    except Exception:
        service.stop()
        raise
    return browser, service


@pytest.fixture
def user() -> Iterator[User]:
    api = StellarBurgersAPI()
    test_user = api.register_user()
    yield test_user
    api.delete_user(test_user.access_token)


@pytest.fixture
def login_page(driver) -> LoginPage:
    return LoginPage(driver)


@pytest.fixture
def main_page(driver) -> MainPage:
    return MainPage(driver)


@pytest.fixture
def opened_main_page(main_page: MainPage) -> MainPage:
    """Общее предусловие тестов: открытая главная страница (конструктор)."""
    return main_page.open()


@pytest.fixture
def feed_page(driver) -> FeedPage:
    return FeedPage(driver)


@pytest.fixture
def authorized_user(login_page: LoginPage, user: User) -> User:
    login_page.login(user.email, user.password)
    return user


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    report = yield
    setattr(item, f"rep_{report.when}", report)

    if report.failed and report.when == "call":
        driver = item.funcargs.get("driver")
        browser_name = item.callspec.params.get("browser_name", "unknown") if hasattr(item, "callspec") else "unknown"
        if driver is not None:
            _attach_failure_artifacts(driver, browser_name)

    return report


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    allure_dir = session.config.getoption("--alluredir", default=None)
    if not allure_dir:
        return

    os.makedirs(allure_dir, exist_ok=True)
    environment_path = os.path.join(allure_dir, "environment.properties")
    with open(environment_path, "w", encoding="utf-8") as environment_file:
        environment_file.write(f"BASE_URL={BASE_URL}\n")
        environment_file.write(f"Python={platform.python_version()}\n")
        environment_file.write(f"OS={platform.platform()}\n")


def _attach_failure_artifacts(driver, browser_name: str) -> None:
    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"Screenshot ({browser_name})",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass

    try:
        allure.attach(
            driver.page_source,
            name=f"Page source ({browser_name})",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception:
        pass

    try:
        allure.attach(
            driver.current_url,
            name="Current URL",
            attachment_type=allure.attachment_type.TEXT,
        )
    except Exception:
        pass

    if browser_name == "chrome":
        try:
            logs = driver.get_log("browser")
            if logs:
                allure.attach(
                    json.dumps(logs, ensure_ascii=False, indent=2),
                    name="Browser logs",
                    attachment_type=allure.attachment_type.JSON,
                )
        except Exception:
            pass
