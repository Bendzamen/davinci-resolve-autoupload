# Script for auto upload to uschovna.cz after
# finished rendering in DaVinci Resolve
# Script is triggerded by DaVinci Resolve script trigger function
# Benjamin Lapos 2024

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from time import sleep
import os

logging.basicConfig(filename='script_log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# CONFIGURATION
SENDER_MAIL = "sender@mail.com"
RECEIVER_MAIL = "receiver@mail.com"
BODY_TEXT = "Hello, sending the final version of the video."
FILE_PATH = "/path/to/file"

TIMEOUT_SEC = 1800  # 30 minutes
CHRPATH = '/path/to/chromedriver'

try:
    os.system('say "starting the script"')
    logging.info("starting script.")
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (optional)
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems (optional)
    chrome_options.add_argument("--window-size=1920x1080")  # Set window size (optional)
    chrome_options.add_argument("--start-maximized")  # Ensure the window is maximized (optional)
    driver = webdriver.Chrome(service=Service(CHRPATH), options=chrome_options)
    logging.info("driver init.")

    driver.get("https://www.uschovna.cz/poslat-zasilku")
    logging.info("first page loaded.")

    # click the "I disagree" button
    sleep(2)
    button = driver.find_element(By.XPATH,
                                 "//button[@class='fc-button\
                                 fc-cta-do-not-consent\
                                 fc-secondary-button']")
    button.click()

    # select the file to upload
    sleep(0.5)
    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_input.send_keys(FILE_PATH)

    # fill the senders mail address
    sleep(0.5)
    sender_email_field = driver.find_element(By.ID, "sender_mail")
    sender_email_field.clear()
    sender_email_field.send_keys(SENDER_MAIL)

    # fill the receivers mail address
    sleep(0.5)
    receiver_email_field = driver.find_element(By.ID, "to_email")
    receiver_email_field.clear()
    receiver_email_field.send_keys(RECEIVER_MAIL)

    # fill the body text
    sleep(0.5)
    body_text_field = driver.find_element(By.ID, "zprava")
    body_text_field.clear()
    body_text_field.send_keys(BODY_TEXT)

    # click the send button
    sleep(0.5)
    button = driver.find_element(By.ID, "poslat_zasilku")
    button.click()

    logging.info("fields filled.")
    sleep(5)

    # Wait till the file is uploaded
    # and the page is redirected to the confirmation page
    try:
        WebDriverWait(driver, TIMEOUT_SEC).until(
            EC.url_matches(r"https://www\.uschovna\.cz/zasilka/.+")
        )
        os.system('say "script finished successfully"')
        logging.info("File uploaded and redirected to the confirmation page.")
    except Exception as e:
        os.system('say "script didnt finish at the desired website"')
        logging.info("Failed to upload the file or\
                     redirect to the expected page.")

    driver.quit()
    logging.info("Chrome WebDriver closed successfully.")

except Exception as e:
    os.system('say "the script failed"')
    logging.error(f"An error occurred: {e}", exc_info=True)
