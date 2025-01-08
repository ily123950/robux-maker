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

    # Выполняем поиск
    print("Searching for 'Pls donate'...")
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("Pls donate")
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)  # Даем время странице загрузиться
    print("Search performed.")

    # Проверяем, есть ли результаты поиска
    results = driver.find_elements(By.XPATH, "//ytd-video-renderer")
    if not results:
        print("No search results found!")
    else:
        print(f"Found {len(results)} results.")

    # Открываем фильтры и выбираем "Live" (стримы)
    print("Applying filters for live streams...")
    filter_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ytd-toggle-button-renderer[@id='filter-button']"))
    )
    filter_button.click()

    live_filter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//yt-formatted-string[text()='Live']"))
    )
    live_filter.click()
    print("Live filter applied.")

    # Ожидаем загрузки стримов
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//a[@id='video-title'])[1]"))
    )

    # Берем первый стрим
    print("Fetching the first live stream...")
    first_stream = driver.find_element(By.XPATH, "(//a[@id='video-title'])[1]")
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
