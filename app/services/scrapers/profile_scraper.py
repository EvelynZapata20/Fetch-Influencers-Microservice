"""
TikTok Profile Scraper

This script scrapes TikTok to extract the first 20 video IDs from a user's profile.
It uses Selenium to automate the browser and retrieve video links.
"""
from app.utils.webdriver import init_webdriver
from app.utils.formatters import format_metric
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)

def get_profile_info(profile_url: str) -> dict:
    """
    Scrapes basic profile information and engagement metrics from a TikTok profile.

    Args:
        profile_url (str): The TikTok profile URL.

    Returns:
        dict: Dictionary containing profile metrics including:
            - name: User's display name
            - followers: Number of followers
            - avg_views: Average views across last 20 videos
            - video_ids: List of first 20 video IDs
    """
    
    driver = init_webdriver()
    wait = WebDriverWait(driver, 10)
    profile_data = {}

    try:
        driver.get(profile_url)
        
        name_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2[data-e2e="user-subtitle"]')))
        profile_data['name'] = name_element.text
        
        followers_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'strong[data-e2e="followers-count"]')))
        followers_text = followers_element.text
        profile_data['followers'] = format_metric(followers_text)
        
        view_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'strong[data-e2e="video-views"]')))
        views = [format_metric(element.text) for element in view_elements[:20]]
        profile_data['avg_views'] = sum(views) / len(views) if views else 0

        video_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/video/"]')))
        video_ids = [video.get_attribute("href").split("/video/")[-1] for video in video_elements[:20]]
        profile_data['video_ids'] = video_ids

    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"Error retrieving profile info: {e}")
        return None
    
    except Exception as e:
        logger.error(f"An unexpected error occurred while scraping profile: {e}")
        return None

    finally:
        driver.quit()

    return profile_data