import json
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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

# Функция загрузки cookies
def load_cookies(driver, cookies_file, domain):
    """Загружает cookies для указанного домена"""
    try:
        with open(cookies_file, "r") as file:
            data = json.load(file)

            if "cookies" not in data:
                raise ValueError("Неверный формат cookies.json!")

            for cookie in data["cookies"]:
                if "domain" in cookie and domain not in cookie["domain"]:
                    logging.warning(f"Пропуск cookie {cookie['name']} из-за несовпадения домена.")
                    continue
                
                driver.add_cookie({
                    "name": cookie["name"],
                    "value": cookie["value"],
                    "domain": domain,
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

# 2. Загружаем cookies
logging.info("Загрузка cookies...")
load_cookies(driver, "cookies.json", ".youtube.com")

# 3. Перезагружаем страницу
logging.info("Обновление страницы для применения cookies...")
driver.refresh()
time.sleep(5)

# 4. Проверяем авторизацию
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

# 5. Открываем случайное видео
logging.info("Поиск списка видео...")
try:
    videos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//a[@id="thumbnail" and @href]'))
    )
    video_urls = [video.get_attribute("href") for video in videos if video.get_attribute("href")]
    
    if not video_urls:
        logging.error("Видео не найдены!")
        driver.quit()
        exit()

    random_video = random.choice(video_urls)
    logging.info(f"Открываем случайное видео: {random_video}")
    driver.get(random_video)
    time.sleep(5)

    # 6. Ставим лайк
    logging.info("Попытка поставить лайк...")
    try:
        like_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="like-button"]'))
        )
        like_button.click()
        logging.info("Лайк поставлен!")
    except TimeoutException:
        logging.error("Не удалось найти кнопку лайка!")
except TimeoutException:
    logging.error("Ошибка загрузки видео!")

# Завершение работы
logging.info("Завершение работы...")
driver.quit()
