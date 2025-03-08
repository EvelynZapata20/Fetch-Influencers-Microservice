"""
TikTok Engagement Scraper

This script automates the extraction of likes, comments, shares and saves
from a TikTok video page using Selenium.
"""

from app.utils.driver import init_driver
from app.utils.formatters import format_metric
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_tiktok_video_data(video_url: str) -> dict:
    """
    Scrapes TikTok to extract likes, comments, shares and saves from a video.
    
    Args:
        video_url (str): The TikTok video URL to scrape.
    
    Returns:
        dict: A dictionary containing the extracted data including:
            - likes: Number of likes on the video
            - comments: Number of comments on the video
            - shares: Number of shares of the video
            - saves: Number of saves of the video
    """
    driver = init_driver()
    wait = WebDriverWait(driver, 10)
    data = {}

    try:
        driver.get(video_url)
        
        likes_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="like-count"]')))
        data["likes"] = format_metric(likes_element.text)
        
        comments_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="comment-count"]')))
        data["comments"] = format_metric(comments_element.text)
        
        shares_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="share-count"]')))
        data["shares"] = format_metric(shares_element.text)
        
        saves_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="undefined-count"]')))
        data["saves"] = format_metric(saves_element.text)

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error retrieving video data: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    finally:    
        driver.quit()
    
    return data