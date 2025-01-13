import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from flask import Flask

# Настройки для headless режима
chrome_options = Options()
chrome_options.add_argument("--headless")  # Без графического интерфейса
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Настройка WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Загружаем сайт YouTube
driver.get("https://www.youtube.com")
print("Navigated to YouTube.")

# Поиск 'Pls donate roblox live' без авторизации
print("Searching for 'Pls donate roblox live' without login...")
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

    # Сохраняем ссылку на первое видео
    saved_video_url = first_stream_url

except TimeoutException:
    print("First stream not found or not clickable.")
    driver.quit()
    exit()

# Возвращаемся на главную страницу YouTube
print("Returning to YouTube homepage...")
driver.get("https://www.youtube.com")
time.sleep(3)

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

# Переход по сохраненной ссылке на стрим
print(f"Going to stream: {saved_video_url}")
driver.close()  # Закрываем текущую вкладку
driver = webdriver.Chrome(options=chrome_options)  # Открываем новый браузер
driver.get(saved_video_url)
time.sleep(5)

# Загрузка cookies и перезагрузка страницы
print("Loading cookies and refreshing stream page...")
load_cookies(driver, "cookies.json")
driver.get(saved_video_url)
time.sleep(5)

# Проверка авторизации после загрузки стрима
print("Checking login status after navigating to stream...")
try:
    avatar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@id="avatar-btn"]'))
    )
    if avatar:
        print("Avatar found. Clicking to check logout button.")
        avatar.click()  # Нажимаем на иконку профиля
        time.sleep(2)  # Небольшая задержка для появления меню

        # Проверяем наличие кнопки "Выйти" (на русском или английском)
        logout_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//yt-formatted-string[text()="Выйти" or text()="Sign out"]'))
        )
        if logout_button:
            print("Logout button found. User is fully logged in.")
        else:
            print("Logout button not found. User might not be fully logged in.")
    else:
        print("Avatar not found. User might not be logged in.")
        driver.quit()
        exit()
except TimeoutException:
    print("Login check failed. Please ensure your cookies are valid.")
    driver.quit()
    exit()

# Завершаем работу
print("Done.")
driver.quit()

# Запуск простого HTTP сервера для связи с портом
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    # Получаем порт из переменной окружения
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
