from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

try:
    # Настройка опций для работы в headless режиме
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Без графического интерфейса
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Настроим Selenium для использования с ChromeDriver
    print("Initializing browser...")
    driver = webdriver.Chrome(options=chrome_options)

    # Открываем сайт YouTube
    print("Opening YouTube...")
    driver.get("https://www.youtube.com")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "search_query"))
    )
    print("YouTube loaded successfully.")

    # Выполняем поиск с ключевыми словами
    print("Searching for 'Pls donate roblox live '...")
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("roblox pls donate live")
    search_box.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ytd-video-renderer"))
    )
    print("Search results loaded.")

    # Находим первый результат
    print("Fetching the first result...")
    first_stream = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//a[@id='video-title'])[1]"))
    )
    stream_title = first_stream.get_attribute("title")
    print(f"First Live Stream Title: {stream_title}")

    # Успешно завершено
    print("Success!")

except Exception as e:
    # Если возникает ошибка, выводим ее
    print(f"An error occurred: {e}")

finally:
    # Закрываем браузер
    print("Closing browser...")
    driver.quit()
