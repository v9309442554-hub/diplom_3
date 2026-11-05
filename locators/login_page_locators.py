from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_HEADING = (By.XPATH, "//h2[normalize-space()='Вход']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='text']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Войти']")
