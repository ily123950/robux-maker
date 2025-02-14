import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Настройка Selenium (headless-режим)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск без интерфейса
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Инициализация драйвера
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL YouTube
YOUTUBE_URL = "https://www.youtube.com"

def load_cookies(driver, cookies_file):
    """Загрузка cookies с исправлением параметров"""
    try:
        with open(cookies_file, "r") as file:
            data = json.load(file)

            if "cookies" not in data:
                raise ValueError("Неверный формат cookies.json! Должен быть объект с ключом 'cookies'.")

            for cookie in data["cookies"]:
                if not all(k in cookie for k in ["name", "value", "domain"]):
                    logging.error(f"Пропущены ключевые данные в cookie: {cookie}")
                    continue

                # Исправление параметров cookies
                if cookie["domain"].startswith("www.youtube.com"):
                    cookie["domain"] = ".youtube.com"
                if cookie["name"] in ["SID", "__Secure-1PSID", "__Secure-3PSID"]:
                    cookie["secure"] = True  # SID должен быть защищенным
                if cookie["name"] in ["APISID", "SAPISID"]:
                    cookie["httpOnly"] = True  # Лучше сделать защищенным

                driver.add_cookie(cookie)

            logging.info("✅ Cookies загружены успешно.")
            time.sleep(5)  # Задержка перед проверкой авторизации

    except FileNotFoundError:
        logging.error("❌ Файл cookies.json не найден!")
    except json.JSONDecodeError:
        logging.error("❌ Ошибка парсинга cookies.json! Проверь формат.")
    except Exception as e:
        logging.error(f"❌ Ошибка загрузки cookies: {e}")

def check_auth(driver):
    """Проверка авторизации на YouTube"""
    driver.get(YOUTUBE_URL)
    time.sleep(5)  # Даем время на загрузку

    # Проверяем, есть ли кнопка "Войти" (если есть — не авторизован)
    if "signin" in driver.page_source.lower():
        logging.error("❌ Ошибка авторизации! Проверь cookies.")
        return False
    logging.info("✅ Авторизация успешна!")
    return True

def main():
    try:
        logging.info("🚀 Запуск скрипта...")
        
        # Открываем YouTube
        driver.get(YOUTUBE_URL)
        time.sleep(5)

        # Загружаем cookies
        logging.info("🔄 Загрузка cookies...")
        load_cookies(driver, "cookies.json")

        # Проверяем авторизацию
        if check_auth(driver):
            logging.info("🎉 Все работает! YouTube авторизован.")
        else:
            logging.error("⚠️ Авторизация не удалась. Проверь cookies.")

    except Exception as e:
        logging.error(f"❌ Ошибка в скрипте: {e}")

    finally:
        driver.quit()
        logging.info("🛑 Скрипт завершил работу.")

# Запуск основного кода
if __name__ == "__main__":
    main()
