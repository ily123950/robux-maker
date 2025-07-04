from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
import pickle
import os

# Telegram токен
TELEGRAM_TOKEN = os.getenv("7841865896:AAEXPcW63zYfbNODVhhvH5QWdHCQAt_khHM")
CHAT_ID_FILE = "chat_id.txt"

def get_chat_id():
    if os.path.exists(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, "r") as f:
            return f.read().strip()
    else:
        print("⏳ Ожидаю первое сообщение от тебя в Telegram...")
        while True:
            try:
                r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates")
                data = r.json()
                if "result" in data and len(data["result"]) > 0:
                    chat_id = str(data["result"][-1]["message"]["chat"]["id"])
                    with open(CHAT_ID_FILE, "w") as f:
                        f.write(chat_id)
                    print(f"✅ Найден chat_id: {chat_id}")
                    return chat_id
            except Exception as e:
                print("Ошибка при получении chat_id:", e)
            time.sleep(5)

def send_telegram_message(text):
    chat_id = get_chat_id()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': chat_id, 'text': text})

# Настройки Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

# Загрузка FanPay
driver.get("https://www.fanpay.ru/messages")
time.sleep(2)

# Загрузка куки
if os.path.exists("cookies.pkl"):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(2)

last_message = ""

while True:
    try:
        driver.get("https://www.fanpay.ru/messages")
        time.sleep(5)

        messages = driver.find_elements(By.CLASS_NAME, "message__text")
        if messages:
            current = messages[-1].text
            if current != last_message:
                send_telegram_message(f"📩 Новое сообщение:\n\n{current}")
                last_message = current
    except Exception as e:
        print("Ошибка:", e)

    time.sleep(30)
