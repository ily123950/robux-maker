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
chrome_options.add_argument('--headless')  # Без графического интерфейса
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
    
    # Перед добавлением cookies убедимся, что мы находимся на правильном домене
    for cookie in cookies:
        if cookie['domain'] == '.youtube.com':  # Убедитесь, что домен совпадает
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
time.sleep(2)  # Даем время для применения cookies

# Переходим на сайт YouTube (снова), чтобы cookies были применены
driver.get("https://www.youtube.com")
time.sleep(3)  # Ждем, пока страница прогрузится после добавления cookies

# Функция для ожидания загрузки страницы
def wait_for_page_load():
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, 'ytd-masthead'))
        )
        print("Page loaded successfully.")
    except TimeoutException:
        print("Page did not load in time.")

# Ждем, пока YouTube загрузится
print("Waiting for YouTube page to load...")
wait_for_page_load()

# Ищем "Pls donate roblox live"
print("Searching for 'Pls donate roblox live'...")
search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys("Pls donate roblox live")
search_box.send_keys(Keys.RETURN)
print("Search initiated.")
time.sleep(3)  # Ждем загрузки результатов

# Ждем загрузки страницы с результатами поиска
wait_for_page_load()

# Ищем первый стрим и выводим его название и ссылку
try:
    print("Waiting for the first video link to be visible...")
    first_stream = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//a[@id="video-title"]'))
    )
    
    # Извлекаем название первого стрима
    first_stream_title = first_stream.get_attribute('title')
    if first_stream_title:
        print(f"First stream title: {first_stream_title}")  # Выводим название стрима
        
        # Извлекаем ссылку на первый стрим
        first_stream_url = first_stream.get_attribute('href')
        print(f"First stream URL: {first_stream_url}")  # Выводим ссылку на стрим
        
        # Закрываем текущую вкладку
        driver.close()
        print("Current tab closed.")
        
        # Открываем новую вкладку с полученной ссылкой
        driver = webdriver.Chrome(options=chrome_options)  # Открываем новый экземпляр браузера
        driver.get(first_stream_url)
        print("Opened the first stream in a new tab.")
    else:
        print("First stream title is not available.")
        driver.quit()
        exit()
        
except TimeoutException:
    print("First video link not found or not clickable.")
    driver.quit()
    exit()

time.sleep(5)  # Ждем, пока откроется видео

# Открываем чат и пишем сообщения
try:
    print("Attempting to open the chat...")
    chat_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="chat"]'))
    )
    print("Chat is available. Scrolling into view...")
    driver.execute_script("arguments[0].scrollIntoView(true);", chat_button)  # Прокрутка к чату
    time.sleep(2)  # Ждем после прокрутки
    
    # Пишем сообщения в чат каждые 3 секунды в течение 5 минут
    end_time = time.time() + 300  # 5 минут
    while time.time() < end_time:
        try:
            print("Finding chat input...")
            chat_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="input"]'))
            )
            chat_input.send_keys("gamernoobikyt")  # Ваше сообщение
            chat_input.send_keys(Keys.RETURN)
            print("Message sent: gamernoobikyt")
            time.sleep(3)  # Ждем 3 секунды
        except Exception as e:
            print(f"Error sending message: {e}")
            break

    print("Finished sending messages.")
except Exception as e:
    print(f"Error interacting with the chat: {e}")
finally:
    driver.quit()
