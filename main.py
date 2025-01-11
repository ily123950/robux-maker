import json
import time
from random import sample
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Настройки для headless режима
chrome_options = Options()
chrome_options.add_argument("--headless")  # Без графического интерфейса
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Настройка WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Загружаем сайт YouTube
    driver.get("https://www.youtube.com")
    print("Navigated to YouTube.")

    # Загрузка cookies для авторизации
    print("Loading cookies...")
    try:
        with open("cookies.json", "r") as file:
            cookie_data = json.load(file)
            cookies = cookie_data["cookies"]
            for cookie in cookies:
                cookie_dict = {
                    "name": cookie["name"],
                    "value": cookie["value"],
                    "domain": cookie["domain"],
                    "path": cookie.get("path", "/"),
                    "secure": cookie.get("secure", False),
                    "httpOnly": cookie.get("httpOnly", False),
                }
                driver.add_cookie(cookie_dict)
        print("Cookies loaded successfully.")
    except Exception as e:
        print(f"Error loading cookies: {e}")
        driver.quit()
        exit()

    # Перезагружаем сайт, чтобы cookies применились
    driver.get("https://www.youtube.com")
    time.sleep(5)

    # Проверка авторизации
    print("Checking login status...")
    try:
        avatar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="avatar-btn"]'))
        )
        if avatar:
            print("Logged into the account successfully.")
        else:
            print("Not logged in. Please check your cookies.")
            driver.quit()
            exit()
    except TimeoutException:
        print("Login check failed. Please ensure your cookies are valid.")
        driver.quit()
        exit()

    # Получение названий видео с главной страницы
    print("Fetching random video titles from the homepage...")
    try:
        video_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@id="video-title"]'))
        )

        # Выбираем 3 случайных видео
        if len(video_elements) >= 3:
            random_videos = sample(video_elements, 3)
            for i, video in enumerate(random_videos, start=1):
                print(f"Video {i}: {video.get_attribute('title')}")
        else:
            print("Not enough videos found on the homepage.")

    except TimeoutException:
        print("No videos found on the homepage.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Завершаем работу
    driver.quit()
    print("Done.")
