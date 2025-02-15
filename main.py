import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Фоновый режим
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
)

logging.info("Запуск WebDriver...")
driver = webdriver.Chrome(options=chrome_options)

def load_cookies(driver, cookies_file):
    """Загружает куки из файла без изменений"""
    try:
        with open(cookies_file, "r") as file:
            cookies = json.load(file)
            driver.get("https://www.youtube.com")  
            time.sleep(2)  

            for cookie in cookies:
                driver.add_cookie(cookie)

            logging.info("Cookies загружены.")
    except Exception as e:
        logging.error(f"Ошибка загрузки cookies: {e}")

def is_logged_in(driver):
    """Проверяет, залогинен ли пользователь"""
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "avatar-btn")))
        return True
    except TimeoutException:
        return False

video_url = "https://www.youtube.com/watch?v=nq1GqSVQzeU"
logging.info(f"Открытие видео: {video_url}")
driver.get(video_url)
time.sleep(5)

logging.info("Загрузка cookies...")
load_cookies(driver, "cookies.json")
driver.refresh()
time.sleep(5)

if is_logged_in(driver):
    logging.info("Авторизован, ставим лайк...")
    try:
        like_button_xpath = "//button[@aria-label='Нравится']"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, like_button_xpath))).click()
        logging.info("Лайк поставлен!")
    except TimeoutException:
        logging.error("Не удалось поставить лайк.")
else:
    logging.error("Авторизация не найдена.")

driver.quit()
