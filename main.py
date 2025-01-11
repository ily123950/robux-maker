import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Настройки для headless режима
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Настройка WebDriver
driver = webdriver.Chrome(options=chrome_options)

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
    # Проверяем наличие аватара пользователя
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@id="avatar-btn"]'))
    )
    print("Logged into the account successfully.")
except TimeoutException as e:
    error_message = f"Login check failed. Please ensure your cookies are valid. Error: {str(e)}"
    print(error_message)
    driver.quit()
    exit()

# Поиск и выбор стрима
print("Searching for 'Pls donate roblox live'...")
search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys("Pls donate roblox live")
search_box.send_keys(Keys.RETURN)
time.sleep(5)

# Ожидание загрузки результатов поиска
print("Waiting for search results...")
try:
    first_stream = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="video-title"]'))
    )
    first_stream_title = first_stream.get_attribute("title")
    first_stream_url = first_stream.get_attribute("href")

    print(f"First stream title: {first_stream_title}")
    print(f"First stream URL: {first_stream_url}")

    # Закрытие текущей вкладки и открытие новой
    driver.close()
    driver.switch_to.new_window('tab')
    driver.get(first_stream_url)
    time.sleep(5)
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
