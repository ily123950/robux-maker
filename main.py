import json
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

    # Открываем YouTube, чтобы загрузить cookies
    print("Opening YouTube...")
    driver.get("https://www.youtube.com")

    # Загрузка cookies из файла
    print("Loading cookies...")
    with open("cookies.json", "r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    print("Cookies loaded successfully.")

    # Обновляем страницу после добавления cookies
    driver.refresh()
    print("Refreshed page after adding cookies.")

    # Выполняем поиск с ключевыми словами
    print("Searching for 'Pls donate roblox live'...")
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("Pls donate roblox live")
    search_box.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ytd-video-renderer"))
    )
    print("Search results loaded.")

    # Находим первый результат и переходим на стрим
    print("Fetching the first result...")
    first_stream = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//a[@id='video-title'])[1]"))
    )
    stream_url = first_stream.get_attribute("href")
    print(f"First Live Stream URL: {stream_url}")
    print("Opening the first stream...")
    driver.get(stream_url)

    # Ожидание загрузки чата
    print("Waiting for chat to load...")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "chatframe"))
    )
    print("Chat loaded successfully.")

    # Переключаемся на iframe чата
    chat_iframe = driver.find_element(By.ID, "chatframe")
    driver.switch_to.frame(chat_iframe)

    # Отправка сообщения каждые 3 секунды в течение 5 минут
    print("Sending messages in chat...")
    start_time = time.time()
    while time.time() - start_time < 300:  # 5 минут
        try:
            # Находим поле ввода сообщения
            message_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='input']"))
            )
            message_box.click()
            message_box.send_keys("gamernoobikyt")
            message_box.send_keys(Keys.RETURN)
            print("Message sent: gamernoobikyt")
        except Exception as e:
            print(f"An error occurred while sending a message: {e}")
        time.sleep(3)  # Задержка между сообщениями

    print("Finished sending messages.")

except Exception as e:
    # Если возникает ошибка, выводим ее
    print(f"An error occurred: {e}")

finally:
    # Закрываем браузер
    print("Closing browser...")
    driver.quit()
