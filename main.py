import time
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging

# Setup logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

EMAIL = "poco870ily@gmail.com"
PASSWORD = "Aa200733"

# Initialize undetected ChromeDriver
options = uc.ChromeOptions()
options.add_argument("--start-maximized")  
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--headless")  # Uncomment for headless mode

driver = uc.Chrome(options=options)

try:
    # Step 1: Open Google Sign-In Page
    logging.info("Opening Google Sign-In page...")
    driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dru%26next%3D%252F")
    
    # Step 2: Enter Email
    time.sleep(2)
    email_input = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    logging.info("Entering email...")
    email_input.send_keys(EMAIL)
    email_input.send_keys(Keys.ENTER)

    # Step 3: Wait for Password Field
    time.sleep(3)
    password_input = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input')
    logging.info("Entering password...")
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.ENTER)

    # Step 4: Wait for login process to complete
    time.sleep(5)
    logging.info("Login process completed.")

    # Step 5: Navigate to YouTube
    driver.get("https://www.youtube.com")
    logging.info("Successfully logged in and navigated to YouTube!")

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")

finally:
    input("Press Enter to close the browser...")  # Keeps the browser open for review
    driver.quit()
