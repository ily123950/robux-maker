import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Настраиваем логи
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Настройки Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless=new")  # Запуск в headless-режиме
chrome_options.add_argument("--enable-logging")  # Включаем логи
chrome_options.add_argument("--v=1")  # Уровень логирования
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# Подключаем ChromeDriver с сервисом логирования
service = Service("/usr/bin/chromedriver")  # Укажи правильный путь, если нужно
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ссылка на стрим
stream_url = "https://www.youtube.com/live/Y3fdeGo0VHA"

# Переход на стрим
logging.info(f"Переход по ссылке: {stream_url}")
driver.get(stream_url)
time.sleep(5)

# Функция для загрузки cookies
def load_cookies(driver, cookies_file):
    """Загрузка cookies в браузер."""
    try:
        with open(cookies_file, "r") as file:
            cookie_data = json.load(file)["cookies"]
            for cookie in cookie_data:
                driver.add_cookie(cookie)
        logging.info("Cookies загружены успешно.")
    except Exception as e:
        logging.error(f"Ошибка загрузки cookies: {e}")

# Загрузка cookies
logging.info("Загрузка cookies...")
load_cookies(driver, "cookies.json")

# Перезагрузка страницы
logging.info("Обновление страницы для применения cookies...")
driver.refresh()
time.sleep(5)

# Проверка авторизации
logging.info("Проверка авторизации...")
try:
    avatar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@id="avatar-btn"]'))
    )
    logging.info("Авторизация успешна.")
except TimeoutException:
    logging.error("Ошибка авторизации. Проверь cookies.")
    driver.quit()
    exit()

# Переход к чату и отправка сообщения
logging.info("Попытка переключиться на чат...")
try:
    chat_iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[@id="chatframe"]'))
    )
    driver.switch_to.frame(chat_iframe)

    logging.info("Поиск поля ввода сообщения в чате...")
    comment_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="input"]'))
    )

    if comment_box.is_displayed() and comment_box.is_enabled():
        logging.info("Поле ввода найдено, отправка сообщения...")
        comment_box.click()
        comment_box.send_keys("test")
        comment_box.send_keys(Keys.RETURN)
        logging.info("Сообщение отправлено: test")
    else:
        logging.warning("Поле ввода чата неактивно.")
except (TimeoutException, NoSuchElementException) as e:
    logging.error(f"Ошибка работы с чатом: {e}")

# Сохранение скриншота (если надо)
screenshot_path = "screenshot.png"
driver.save_screenshot(screenshot_path)
logging.info(f"Скриншот сохранён: {screenshot_path}")

# Завершаем работу
logging.info("Тест завершён.")
driver.quit()
