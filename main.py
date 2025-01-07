from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Настройка опций для работы в headless режиме
chrome_options = Options()
chrome_options.add_argument('--headless')  # Без графического интерфейса
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Настроим Selenium для использования с ChromeDriver
driver = webdriver.Chrome(options=chrome_options)

# Открываем сайт
driver.get("https://www.youtube.com")
print(driver.title)  # Печатаем заголовок страницы

# Даем время на выполнение
time.sleep(3)

# Закрываем браузер
driver.quit()