import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from flask import Flask

# Настройки для headless режима
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Функция для преобразования формата cookies
def transform_cookies(cookies_file):
    """Преобразование cookies из расширенного формата в формат Selenium."""
    try:
        with open(cookies_file, "r") as file:
            data = json.load(file)
            transformed_cookies = [
                {
                    "name": cookie["name"],
                    "value": cookie["value"],
                    "domain": cookie["domain"],
                    "path": cookie.get("path", "/"),
                    "secure": cookie.get("secure", False),
                    "httpOnly": cookie.get("httpOnly", False),
                }
                for cookie in data.get("cookies", [])
            ]
            return transformed_cookies
    except Exception as e:
        print(f"Error transforming cookies: {e}")
        return []

# Функция для загрузки cookies в WebDriver
def load_cookies(driver, cookies_file):
    """Загрузка cookies в браузер."""
    cookies = transform_cookies(cookies_file)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Error adding cookie: {e}")

# Функция для проверки авторизации
def check_login(driver):
    """Проверка, авторизован ли пользователь."""
    try:
        avatar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="avatar-btn"]'))
        )
        return True if avatar else False
    except TimeoutException:
        return False

# Настройка WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Переход на стрим
stream_url = "https://www.youtube.com/live/w52ZoLpxDe0?si=UpDo4GPHuAbCuZXl"
driver.get(stream_url)
time.sleep(5)

# Загрузка cookies
load_cookies(driver, "cookies.json")
driver.get(stream_url)  # Перезагрузка страницы после загрузки cookies
time.sleep(5)

# Проверка авторизации
if check_login(driver):
    print("Successfully logged in.")

    # Ожидание загрузки чата
    try:
        print("Waiting for chat iframe...")
        chat_frame = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="chatframe"]'))
        )
        driver.switch_to.frame(chat_frame)  # Переключаемся на iframe
        print("Switched to chat iframe.")

        # Проверяем наличие поля для ввода сообщения
        comment_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="input"]'))
        )

        # Пишем сообщение в чат
        comment_box.click()
        comment_box.send_keys("test")
        comment_box.send_keys(Keys.RETURN)
        print("Message sent: test")
    except Exception as e:
        print(f"Error interacting with chat: {e}")
    finally:
        driver.switch_to.default_content()
else:
    print("Failed to log in. Please check your cookies.")

# Завершаем работу
print("Done.")
driver.quit()

# Запуск простого HTTP сервера
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
