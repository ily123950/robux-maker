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
chrome_options.add_argument("--headless")  # Без графического интерфейса
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Настройка WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Загружаем сайт YouTube
    driver.get("https://www.youtube.com")
    print("Navigated to YouTube.")

    # Выполняем поиск по запросу
    print("Searching for 'Pls donate roblox live'...")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "search_query"))
    )
    search_box.send_keys("Pls donate roblox live")
    search_box.send_keys(Keys.RETURN)

    # Ожидание загрузки результатов поиска
    print("Waiting for search results...")
    time.sleep(5)  # Небольшая задержка для загрузки результатов

    # Получаем первый стрим из результатов поиска
    try:
        first_stream = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="video-title"]'))
        )
        first_stream_title = first_stream.get_attribute("title")
        first_stream_url = first_stream.get_attribute("href")

        if first_stream_title and first_stream_url:
            print(f"First stream title: {first_stream_title}")
            print(f"First stream URL: {first_stream_url}")
        else:
            print("First stream title or URL not found.")
    except TimeoutException:
        print("No streams found for the search query.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Завершаем работу
    driver.quit()
    print("Done.")
