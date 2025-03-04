"""
TikTok Engagement Scraper

This script automates the extraction of likes, comments, shares and saves
from a TikTok video page using Selenium.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_tiktok_video_data(video_url: str) -> dict:
    """
    Scrapes TikTok to extract likes, comments, shares and saves from a video.
    
    Args:
        video_url (str): The TikTok video URL to scrape.
    
    Returns:
        dict: A dictionary containing the extracted data.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("--log-level=3")  
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    data = {}

    try:
        driver.get(video_url)
        time.sleep(5)
        
        data["likes"] = driver.find_element(By.CSS_SELECTOR, '[data-e2e="like-count"]').text
        data["comments"] = driver.find_element(By.CSS_SELECTOR, '[data-e2e="comment-count"]').text
        data["shares"] = driver.find_element(By.CSS_SELECTOR, '[data-e2e="share-count"]').text
        data["saves"] = driver.find_element(By.CSS_SELECTOR, '[data-e2e="undefined-count"]').text

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:    
        driver.quit()
    
    return data