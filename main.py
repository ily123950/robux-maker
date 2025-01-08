import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Настройка опций для работы в headless режиме
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Настроим Selenium для использования с ChromeDriver
driver = webdriver.Chrome(options=chrome_options)

# Переходим на сайт YouTube
driver.get("https://www.youtube.com")
print("Navigated to YouTube.")

# Логируем загрузку cookies
print("Loading cookies...")
with open("cookies.json", "r") as file:
    cookie_data = json.load(file)
    cookies = cookie_data['cookies']
    for cookie in cookies:
        if cookie['domain'] == '.youtube.com':
            cookie_dict = {
                'name': cookie['name'],
                'value': cookie['value'],
                'domain': cookie['domain'],
                'path': cookie.get('path', '/'),
                'secure': cookie.get('secure', False),
                'httpOnly': cookie.get('httpOnly', False)
            }
            driver.add_cookie(cookie_dict)

print("Cookies loaded successfully.")
time.sleep(2)
driver.get("https://www.youtube.com")
time.sleep(3)

# Проверка авторизации
def check_authorization(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="avatar-btn"]'))
        )
        print("User is logged in.")
        return True
    except TimeoutException:
        print("User is not logged in.")
        return False

if not check_authorization(driver):
    print("Authorization failed. Please ensure your cookies are valid.")
    driver.quit()
    exit()

# Ищем и открываем первый стрим
print("Searching for 'Pls donate roblox live'...")
search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys("Pls donate roblox live")
search_box.send_keys(Keys.RETURN)
time.sleep(3)

try:
    first_stream = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//a[@id="video-title"]'))
    )
    first_stream_title = first_stream.get_attribute('title')
    first_stream_url = first_stream.get_attribute('href')
    print(f"First stream title: {first_stream_title}")
    print(f"First stream URL: {first_stream_url}")

    driver.get(first_stream_url)
    print("Opened the first stream.")
except TimeoutException:
    print("First stream not found.")
    driver.quit()
    exit()

time.sleep(5)

# Прокрутка до поля для ввода комментариев и ввод текста
try:
    print("Locating comment box...")
    comment_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="input"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", comment_box)
    print("Scrolled to comment box.")

    # Ввод сообщения
    comment_box.send_keys("gamernoobikyt")
    comment_box.send_keys(Keys.RETURN)
    print("Comment posted.")
except TimeoutException:
    print("Comment box not found.")
except Exception as e:
    print(f"Error interacting with comment box: {e}")

# Завершаем работу
driver.quit()
