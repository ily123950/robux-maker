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

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--disk-cache-size=0")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
)

def start_driver():
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

def process_video(driver, video_url):
    try:
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
                like_button_xpath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]/segmented-like-dislike-button-view-model/yt-smartimation/div/div/like-button-view-model/toggle-button-view-model/button-view-model/button/yt-touch-feedback-shape/div/div[2]"
                
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, like_button_xpath))).click()
                logging.info("Лайк поставлен!")
            except TimeoutException:
                logging.error("Не удалось поставить лайк.")
        else:
            logging.error("Авторизация не найдена.")

    except WebDriverException:
        logging.error("Chrome crashed, перезапускаем WebDriver...")
        driver.quit()
        driver = start_driver()
        process_video(driver, video_url)

video_url = "https://www.youtube.com/watch?v=nq1GqSVQzeU"

driver = start_driver()
process_video(driver, video_url)

driver.quit()
