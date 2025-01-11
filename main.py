import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Настройки для headless режима
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Настройка WebDriver
try:
    driver = webdriver.Chrome(options=chrome_options)
except WebDriverException as e:
    print(f"Error initializing WebDriver: {e}")
    exit()

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
            driver.add_cookie({
                "name": cookie["name"],
                "value": cookie["value"],
                "domain": cookie["domain"],
                "path": cookie.get("path", "/"),
                "secure": cookie.get("secure", False),
                "httpOnly": cookie.get("httpOnly", False),
            })
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
    if avatar.is_displayed():
        print("Logged into the account successfully.")
    else:
        print("Avatar not visible, login might have failed.")
except TimeoutException as e:
    print(f"Login check failed. Please ensure your cookies are valid. Error: {str(e)}")
    driver.quit()
    exit()

# Поиск и выбор стрима
print("Searching for 'Pls donate roblox live'...")
try:
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "search_query"))
    )
    search_box.send_keys("Pls donate roblox live")
    search_box.submit()  # Нажимаем Enter
    print("Search submitted.")
    time.sleep(5)

    print("Waiting for search results...")
    first_stream = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="video-title"]'))
    )
    first_stream_title = first_stream.get_attribute("title")
    first_stream_url = first_stream.get_attribute("href")

    if first_stream_url:
        print(f"First stream title: {first_stream_title}")
        print(f"First stream URL: {first_stream_url}")
        driver.get(first_stream_url)  # Переходим на страницу стрима
        time.sleep(5)
    else:
        print("Stream URL not found.")
        driver.quit()
        exit()
except TimeoutException as e:
    print(f"First stream not found or not clickable. Error: {str(e)}")
    driver.quit()
    exit()

# Работа с комментариями
print("Waiting for comment box...")
try:
    comment_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="input"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", comment_box)
    time.sleep(1)

    if comment_box.is_displayed() and comment_box.is_enabled():
        comment_box.click()
        comment_box.send_keys("gamernoobikyt")
        comment_box.send_keys(Keys.RETURN)
        print("Message sent: gamernoobikyt")
    else:
        print("Comment box is not interactable.")
except Exception as e:
    print(f"Error interacting with the comment box: {e}")

# Завершаем работу
print("Done.")
driver.quit()
