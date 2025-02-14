import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Настройка логов
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Настройки Chrome (headless-режим)
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920x1080")

# User-Agent Android 14 (Chrome 133, Xiaomi 22021211RG)
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Linux; Android 14; 22021211RG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36"
)

# Запуск WebDriver
logging.info("Запуск WebDriver...")
driver = webdriver.Chrome(options=chrome_options)

# Функция загрузки cookies
def load_cookies(driver, cookies_file):
    """Загрузка cookies с исправлением домена"""
    try:
        with open(cookies_file, "r") as file:
            data = json.load(file)

            if "cookies" not in data:
                raise ValueError("Неверный формат cookies.json! Должен быть объект с ключом 'cookies'.")

            for cookie in data["cookies"]:
                if not all(k in cookie for k in ["name", "value"]):
                    logging.error(f"Пропущены ключевые данные в cookie: {cookie}")
                    continue

                # Принудительно устанавливаем правильный домен
                cookie["domain"] = ".youtube.com"

                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    logging.error(f"Ошибка добавления cookie {cookie['name']}: {e}")

            logging.info("Cookies загружены успешно.")
    except FileNotFoundError:
        logging.error("Файл cookies.json не найден!")
    except json.JSONDecodeError:
        logging.error("Ошибка парсинга cookies.json! Проверь формат.")
    except Exception as e:
        logging.error(f"Ошибка загрузки cookies: {e}")

# Открытие YouTube
logging.info("Открытие YouTube...")
driver.get("https://www.youtube.com")
time.sleep(3)

# Загрузка cookies
logging.info("Загрузка cookies...")
load_cookies(driver, "cookies.json")

# Перезагрузка страницы для применения cookies
logging.info("Обновление страницы для применения cookies...")
driver.refresh()
time.sleep(5)

# Проверка авторизации
logging.info("Проверка авторизации...")
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@id="avatar-btn"]'))
    )
    logging.info("Авторизация успешна!")
except TimeoutException:
    logging.error("Ошибка авторизации. Проверь cookies.")
    driver.quit()
    exit()

# Открытие стрима
stream_url = "https://www.youtube.com/live/Y3fdeGo0VHA"
logging.info(f"Переход по ссылке: {stream_url}")
driver.get(stream_url)
time.sleep(5)

# Переход в чат и отправка сообщения
logging.info("Поиск iframe чата...")
try:
    chat_iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[@id="chatframe"]'))
    )
    driver.switch_to.frame(chat_iframe)

    logging.info("Поиск поля ввода чата...")
    comment_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="input"]'))
    )

    if comment_box.is_displayed() and comment_box.is_enabled():
        logging.info("Поле чата найдено. Отправка сообщения...")
        comment_box.click()
        comment_box.send_keys("test")
        comment_box.send_keys(Keys.RETURN)
        logging.info("Сообщение отправлено!")
    else:
        logging.error("Поле чата неактивно!")
except TimeoutException:
    logging.error("Не найден iframe чата или поле ввода!")
except NoSuchElementException:
    logging.error("Элемент не найден в чате!")

# Завершение работы
logging.info("Тест завершён.")
driver.quit()
