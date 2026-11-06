# Stellar Burgers — UI-автотесты

Дипломный проект: UI-тесты веб-приложения [Stellar Burgers](https://stellarburgers.education-services.ru/).
Проект построен на паттерне Page Object, запускается в Google Chrome и Mozilla Firefox, результаты
сохраняются в Allure-отчёт.

## Стек

- Python 3.10+
- Selenium WebDriver 4
- pytest
- allure-pytest
- requests (создание и удаление тестовых пользователей через API)

## Структура проекта

```text
.
├── conftest.py                  # фикстуры браузера, пользователя, скриншоты при падении
├── locators/                    # локаторы страниц
├── pages/                       # Page Object-классы
│   ├── base_page.py
│   ├── main_page.py             # конструктор бургера
│   ├── feed_page.py             # лента заказов
│   └── login_page.py
├── tests/
│   ├── test_constructor.py      # навигация, модальное окно, счётчик ингредиента
│   └── test_order_feed.py       # счётчики ленты, заказ в разделе «В работе»
├── utils/
│   ├── api_client.py            # создание и удаление тестового пользователя
│   ├── config.py                # настройки из переменных окружения
│   ├── test_data.py             # тестовые данные и ожидаемые тексты
│   └── urls.py                  # пути страниц и сборка адресов с BASE_URL
├── pytest.ini
└── requirements.txt
```

## Установка

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Selenium Manager автоматически подбирает и скачивает драйверы для установленных браузеров.

Тестовый пользователь регистрируется через API перед тестом и удаляется после его завершения,
поэтому тесты не зависят друг от друга и не оставляют данных в приложении.

## Запуск тестов

Все тесты в Chrome и Firefox:

```bash
pytest
```

Только в одном браузере:

```bash
pytest --browser chrome
pytest --browser firefox
```

С видимым окном браузера:

```bash
pytest --headed
```

По умолчанию браузеры запускаются в headless-режиме. Отключить его можно также переменной окружения:

```powershell
$env:HEADLESS = "false"
pytest
```

## Allure-отчёт

Результаты прогона сохраняются в `allure-results` (каталог очищается перед запуском)
и хранятся в репозитории, чтобы результат последнего прогона был доступен без перезапуска тестов.

Просмотр отчёта:

```bash
allure serve allure-results
```

Генерация статического отчёта:

```bash
allure generate allure-results -o allure-report --clean
```

При падении теста в отчёт автоматически прикладываются скриншот, HTML-страницы и текущий URL,
а для Chrome — ещё и логи браузера.

## Настройки

Переменные окружения:

| Переменная | Значение по умолчанию | Назначение |
| --- | --- | --- |
| `BASE_URL` | `https://stellarburgers.education-services.ru` | Адрес тестируемого приложения |
| `HEADLESS` | `true` | Запуск браузера без окна |
| `DEFAULT_TIMEOUT` | `10` | Базовое ожидание элементов, секунды |
| `LONG_TIMEOUT` | `30` | Ожидание обновления ленты заказов, секунды |
| `WINDOW_WIDTH` | `1920` | Ширина окна браузера |
| `WINDOW_HEIGHT` | `1080` | Высота окна браузера |
