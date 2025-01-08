import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

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

# Дальше выполняем остальные действия (поиск, выбор стрима и т.д.)
# Ищем "Pls donate roblox live"
print("Searching for 'Pls donate roblox live'...")
search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys("Pls donate roblox live")
search_box.send_keys(Keys.RETURN)
print("Search initiated.")
time.sleep(3)  # Ждем загрузки результатов

# Переходим на первый стрим
print("Selecting the first live stream...")
first_stream = driver.find_element(By.XPATH, '//*[@id="video-title"]')
first_stream.click()
print("Clicked on the first live stream.")
time.sleep(5)  # Ждем, пока откроется видео

# Открываем чат, если он скрыт
try:
    print("Attempting to open the chat...")
    chat_button = driver.find_element(By.XPATH, '//*[@id="chat"]/div/div[1]/div[2]/button')
    chat_button.click()
    print("Chat opened.")
    time.sleep(2)  # Ждем, пока чат откроется
except Exception as e:
    print(f"Error opening chat: {e}")

# Пишем сообщение в чат каждые 3 секунды в течение 5 минут
end_time = time.time() + 300  # 5 минут
print("Sending messages to chat every 3 seconds for 5 minutes.")
while time.time() < end_time:
    try:
        print("Finding chat input...")
        chat_input = driver.find_element(By.XPATH, '//*[@id="input"]')
        chat_input.send_keys("gamernoobikyt")  # Ваше сообщение
        chat_input.send_keys(Keys.RETURN)
        print("Message sent: gamernoobikyt")
        time.sleep(3)  # Ждем 3 секунды
    except Exception as e:
        print(f"Error sending message: {e}")
        break

print("Finished sending messages.")
driver.quit()
