"""
TikTok Message Sender

This script automates sending messages to TikTok profiles using Selenium.
It handles the message sending process with proper delays and error handling.
"""

import logging
import random
import time
import re

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from app.utils.web_driver import WebDriverManager

logger = logging.getLogger(__name__)

def clean_message(message: str) -> str:
    """
    Clean the message to ensure it only contains BMP Unicode characters.
    
    Args:
        message (str): The original message.
    
    Returns:
        str: The cleaned message with only BMP characters.
    """
    # Remove or replace non-BMP characters (characters outside U+0000 to U+FFFF)
    return ''.join(c for c in message if ord(c) < 0x10000)

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
    success = False

    try:
        # Clean the message before sending
        cleaned_message = clean_message(message)
        if cleaned_message != message:
            logger.warning("Some characters were removed from the message due to Unicode limitations")
        
        driver.get(profile_url)
        time.sleep(random.uniform(2, 5))

        message_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-e2e="message-button"]')
            )
        )
        message_button.click()
        time.sleep(random.uniform(1, 3))

        logger.info("Message button clicked.")
                
        editable = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div[data-e2e='message-input-area'] div[contenteditable='true']"
            ))
        )

        logger.info("Editable element found.")
        
        editable.click()
        editable.send_keys(cleaned_message + Keys.ENTER)

        logger.info("Message sent successfully.")
        success = True

    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        success = False
    
    finally:
        try:
            time.sleep(5)
            # Always attempt to close the driver
            WebDriverManager.close_driver()
            logger.info("Driver closed successfully after message operation")
        except Exception as e:
            logger.error(f"Error while closing driver: {str(e)}")
    
    return success