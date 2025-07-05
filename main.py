from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
import json
import os

# 🔐 Твой Telegram токен (НЕ УДАЛЯЙ ЭТИ СТРОКИ)
TELEGRAM_TOKEN = "7841865896:AAEXPcW63zYfbNODVhhvH5QWdHCQAt_khHM"
CHAT_ID_FILE = "chat_id.txt"

def get_chat_id():
    if os.path.exists(CHAT_ID_FILE):
        with open(CHAT_ID_FILE, "r") as f:
            chat_id = f.read().strip()
            print(f"✅ chat_id найден в файле: {chat_id}")
            return chat_id
    else:
        print("⏳ Жду первое сообщение в Telegram бота...")
        while True:
            try:
                r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates")
                data = r.json()
                if "result" in data and len(data["result"]) > 0:
                    chat_id = str(data["result"][-1]["message"]["chat"]["id"])
                    with open(CHAT_ID_FILE, "w") as f:
                        f.write(chat_id)
                    print(f"✅ Получен chat_id: {chat_id}")
                    return chat_id
                else:
                    print("🔄 Пока нет новых сообщений. Жду...")
            except Exception as e:
                print("❌ Ошибка при получении chat_id:", e)
            time.sleep(5)

def send_telegram_message(text):
    chat_id = get_chat_id()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        response = requests.post(url, data={'chat_id': chat_id, 'text': text})
        if response.status_code == 200:
            print(f"📤 Отправлено в Telegram: {text[:40]}...")
        else:
            print(f"⚠️ Ошибка отправки сообщения: {response.status_code} - {response.text}")
    except Exception as e:
        print("❌ Ошибка при отправке сообщения в Telegram:", e)

# Настройки Chrome
print("🚀 Запуск headless Chrome...")
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

try:
    driver = webdriver.Chrome(options=options)
except Exception as e:
    print("❌ Ошибка запуска Chrome:", e)
    exit()

# Загрузка FanPay
print("🌐 Переход на FanPay...")
driver.get("https://www.fanpay.ru/messages")
time.sleep(2)

# Загрузка cookies из cookies.json
if os.path.exists("cookies.json"):
    print("🍪 Загружаем cookies.json...")
    try:
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            cookie.pop("sameSite", None)  # иногда мешает
            driver.add_cookie(cookie)
        driver.refresh()
        print("✅ Cookies применены.")
        time.sleep(2)
    except Exception as e:
        print("❌ Ошибка загрузки cookies.json:", e)
else:
    print("⚠️ cookies.json не найден!")

# Цикл отслеживания сообщений
last_message = ""
print("🔁 Начинаю мониторинг сообщений...")

while True:
    try:
        driver.get("https://www.fanpay.ru/messages")
        time.sleep(5)
        print("📥 Ищу новые сообщения...")

        messages = driver.find_elements(By.CLASS_NAME, "message__text")
        print(f"🔎 Найдено сообщений: {len(messages)}")

        if messages:
            current = messages[-1].text.strip()
            if current != last_message:
                print(f"📨 Новое сообщение: {current}")
                send_telegram_message(f"📩 Новое сообщение на FanPay:\n\n{current}")
                last_message = current
            else:
                print("✅ Сообщение не изменилось.")
        else:
            print("❌ Сообщений не найдено (возможно, другой селектор).")

    except Exception as e:
        print("❌ Ошибка в цикле:", e)

    time.sleep(30)
