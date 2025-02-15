import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    )

    logging.info("Запуск WebDriver...")
    return webdriver.Chrome(options=chrome_options)

def load_cookies(driver, cookies_file, domain=".youtube.com"):
    try:
        with open(cookies_file, "r") as file:
            data = json.load(file)
            if "cookies" not in data or not isinstance(data["cookies"], list):
                raise ValueError("Неверный формат cookies.json!")

            valid_cookies = [cookie for cookie in data["cookies"] if domain in cookie.get("domain", "")]
            if not valid_cookies:
                raise ValueError(f"В файле нет куки для {domain}")

            driver.get(f"https://{domain.strip('.')}/")
            time.sleep(2)

            for cookie in valid_cookies:
                cookie.pop("sameSite", None)  
                driver.add_cookie(cookie)

            logging.info("Cookies загружены.")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        logging.error(f"Ошибка загрузки cookies: {e}")

def is_logged_in(driver):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "avatar-btn")))
        return True
    except TimeoutException:
        return False

def play_video(driver, url):
    logging.info(f"Открытие видео: {url}")
    driver.get(url)
    time.sleep(5)

    logging.info("Загрузка cookies...")
    load_cookies(driver, "cookies.json")
    driver.refresh()
    time.sleep(5)

    if is_logged_in(driver):
        logging.info("Авторизован. Видео запущено.")
    else:
        logging.error("Авторизация не найдена.")

    time.sleep(30)  # Даем видео проиграться 30 секунд

while True:
    try:
        driver = create_driver()
        play_video(driver, "https://www.youtube.com/watch?v=nq1GqSVQzeU")
        break  # Если все прошло без ошибок — выходим из цикла
    except WebDriverException as e:
        logging.error(f"Ошибка WebDriver: {e}, перезапуск...")
        time.sleep(5)
    finally:
        driver.quit()
