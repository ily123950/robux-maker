from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# Настройки Chrome (headless)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Без GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Запуск браузера
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Открываем сайт Roblox
driver.get("https://www.roblox.com/transactions")

# Загружаем куки
with open("cookies.json", "r") as f:
    cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

# Перезагружаем страницу с авторизацией
driver.refresh()

time.sleep(5)  # Ждём загрузку
print(driver.page_source)  # Проверка содержимого

driver.quit()
