"""
TikTok Message Sender

This script automates sending messages to TikTok profiles using Selenium.
It handles the message sending process with proper delays and error handling.
"""

import logging
import random
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from app.utils.web_driver import WebDriverManager

logger = logging.getLogger(__name__)

def send_message(profile_url: str, message: str) -> bool:
    """
    Send a message to a TikTok profile.

    Args:
        profile_url (str): The URL of the TikTok profile to send the message to.
        message (str): The message to send.
    
    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    driver = WebDriverManager.get_driver()
    wait_time = random.uniform(8, 12)
    wait = WebDriverWait(driver, wait_time)

    try:
        driver.get(profile_url)
        time.sleep(random.uniform(2, 5))

        message_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-e2e="message-button"]')
            )
        )
        message_button.click()
        time.sleep(random.uniform(1, 3))
        
        editable = driver.find_element(
            By.CSS_SELECTOR,
            "div[data-e2e='message-input-area'] div[contenteditable='true']"
        )

        editable.click()
        editable.send_keys(message + Keys.ENTER)

        print("Message sent successfully.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False