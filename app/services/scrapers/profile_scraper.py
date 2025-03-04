"""
TikTok Profile Scraper

This script scrapes TikTok to extract the first 20 video IDs from a user's profile.
It uses Selenium to automate the browser and retrieve video links.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

def get_video_links(profile_url: str) -> set:
    """
    Extracts the first 20 video IDs from a TikTok profile.

    Args:
        profile_url (str): The TikTok profile URL.

    Returns:
        list: A list of video IDs from the first 20 videos.
    """    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("--log-level=3")  

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    video_ids = set()

    try:
        driver.get(profile_url)
        time.sleep(5)  

        videos = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/video/"]')

        pattern = re.compile(r"/video/(\d+)$")
        for video in videos:
            link = video.get_attribute("href")
            match = pattern.search(link)
            if match:
                video_ids.add(match.group(1))
            if len(video_ids) >= 20:
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:    
        driver.quit()

    return video_ids