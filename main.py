from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

try:
    # Настройка опций для работы в headless режиме
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Без графического интерфейса
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Настроим Selenium для использования с ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Открываем сайт
    driver.get("https://www.youtube.com")

    # Печатаем заголовок страницы
    title = driver.title
    print(f"Title: {title}")

    # Выводим сообщение об успешном выполнении
    print("Success!")
    
except Exception as e:
    # Если возникает ошибка, выводим ее
    print(f"An error occurred: {e}")

finally:
    # Закрываем браузер
    driver.quit()
