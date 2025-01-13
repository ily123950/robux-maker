import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Настройки для headless режима
chrome_options = Options()
chrome_options.add_argument("--headless")  # Без графического интерфейса
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Настройка WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Ссылка на стрим
stream_url = "https://www.youtube.com/live/Y3fdeGo0VHA"

# Переход на стрим
print(f"Navigating to stream: {stream_url}")
driver.get(stream_url)
time.sleep(5)

# Функция для загрузки cookies
def load_cookies(driver, cookies_file):
    """Загрузка cookies в браузер."""
    try:
        with open(cookies_file, "r") as file:
            cookie_data = json.load(file)["cookies"]
            for cookie in cookie_data:
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

# Загрузка cookies
print("Loading cookies...")
load_cookies(driver, "cookies.json")

# Перезагрузка страницы
print("Refreshing page to apply cookies...")
driver.refresh()
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

# Переход к чату и отправка сообщения
print("Switching to chat iframe...")
try:
    chat_iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[@id="chatframe"]'))
    )
    driver.switch_to.frame(chat_iframe)

    print("Waiting for chat input box...")
    comment_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="input"]'))
    )

    if comment_box.is_displayed() and comment_box.is_enabled():
        print("Comment box found. Sending message...")
        comment_box.click()
        comment_box.send_keys("test")
        comment_box.send_keys(Keys.RETURN)
        print("Message sent: test")
    else:
        print("Comment box is not interactable.")
except TimeoutException:
    print("Chat iframe or input box not found.")
except NoSuchElementException:
    print("Element not found in chat iframe.")

# Завершаем работу
print("Test completed.")
driver.quit()
