import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    # Ищем аватар пользователя
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
except Exception as e:
    print(f"Unexpected error during login check: {str(e)}")
    driver.quit()
    exit()

# Дальнейший код...
