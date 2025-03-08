"""
TikTok Hashtag Scraper

This script automates the extraction of unique usernames from videos 
under a TikTok hashtag page using Selenium
"""
from app.utils.driver import init_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)

def get_usernames(tag_url: str) -> set:
    """
    Scrapes TikTok to extract unique usernames from a hashtag page.
    
    Args:
        url (str): The TikTok tag URL to scrape.
    
    Returns:
        set: A set of unique usernames found on the page.
    """

    driver = init_driver()
    wait = WebDriverWait(driver, 10)
    usernames = set()

    try:
        driver.get(tag_url)
        
        videos = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-e2e="challenge-item"]')))

        for video in videos:
            try:
                username_element = video.find_element(By.CSS_SELECTOR, '[data-e2e="challenge-item-username"]')
                username = username_element.text
                if username:
                    usernames.add(username)
            except NoSuchElementException:
                continue 

    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"Error retrieving hashtag data: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None

    finally:    
        driver.quit()
    
    return usernames
