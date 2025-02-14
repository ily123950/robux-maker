import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Настройка логов
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Настройки Chrome
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
)

# Запуск WebDriver
logging.info("Запуск WebDriver...")
driver = webdriver.Chrome(options=chrome_options)

# Функция проверки авторизации
def is_logged_in(driver):
    """Проверяет, авторизован ли пользователь (по наличию аватарки)."""
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="avatar-btn"]'))
        )
        logging.info("Авторизация обнаружена!")
        return True
    except TimeoutException:
        logging.warning("Авторизация не найдена!")
        return False

# Функция загрузки cookies
def load_cookies(driver, cookies_file, domain):
    """Загружает cookies для указанного домена"""
    try:
        with open(cookies_file, "r") as file:
            data = json.load(file)

            if "cookies" not in data:
                raise ValueError("Неверный формат cookies.json!")

            for cookie in data["cookies"]:
                # Проверяем, что домен совпадает или является поддоменом
                cookie_domain = cookie.get("domain", "")
                if not cookie_domain.startswith("."):
                    cookie_domain = "." + cookie_domain  # Делаем домен универсальным

                if domain.endswith(cookie_domain) or cookie_domain.endswith(domain):
                    driver.add_cookie({
                        "name": cookie["name"],
                        "value": cookie["value"],
                        "domain": cookie_domain,
                        "path": cookie.get("path", "/"),
                        "secure": cookie.get("secure", False),
                        "httpOnly": cookie.get("httpOnly", False),
                    })

            logging.info("Cookies загружены успешно.")
    except FileNotFoundError:
        logging.error("Файл cookies.json не найден!")
    except json.JSONDecodeError:
        logging.error("Ошибка парсинга cookies.json!")
    except Exception as e:
        logging.error(f"Ошибка загрузки cookies: {e}")

# 1. Открываем YouTube
logging.info("Переход на YouTube...")
driver.get("https://www.youtube.com/")
time.sleep(5)

# 2. Проверяем авторизацию
if not is_logged_in(driver):
    logging.info("Загрузка cookies...")
    load_cookies(driver, "cookies.json", ".youtube.com")

    # Перезагружаем страницу
    logging.info("Обновление страницы для применения cookies...")
    driver.refresh()
    time.sleep(5)

# 3. Переходим на видео
video_url = "https://www.youtube.com/watch?v=nq1GqSVQzeU"
logging.info(f"Переход на видео: {video_url}")
driver.get(video_url)
time.sleep(5)

# 4. Проверяем авторизацию ещё раз
if not is_logged_in(driver):
    logging.info("Повторная загрузка cookies...")
    load_cookies(driver, "cookies.json", ".youtube.com")

    # Перезагружаем страницу
    logging.info("Обновление страницы для применения cookies...")
    driver.refresh()
    time.sleep(5)

# 5. Ставим лайк
if is_logged_in(driver):
    logging.info("Попытка поставить лайк...")
    try:
        like_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="like-button"]'))
        )
        like_button.click()
        logging.info("Лайк поставлен!")
    except TimeoutException:
        logging.error("Не удалось найти кнопку лайка!")

# Завершение работы
logging.info("Завершение работы...")
driver.quit()
