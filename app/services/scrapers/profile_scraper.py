"""
TikTok Profile Scraper

This script scrapes TikTok to extract the first 20 video IDs from a user's profile.
It uses Selenium to automate the browser and retrieve video links.
"""
from app.utils.driver import init_driver
from app.utils.formatters import format_metric
from selenium.webdriver.common.by import By
import time



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
    """
    driver = init_driver()
    profile_data = {}

    try:
        driver.get(profile_url)
        time.sleep(5) 

        profile_data['name'] = driver.find_element(By.CSS_SELECTOR, 'h2[data-e2e="user-subtitle"]').text
        followers_text = driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="followers-count"]').text
        profile_data['followers'] = format_metric(followers_text)
        view_elements = driver.find_elements(By.CSS_SELECTOR, 'strong[data-e2e="video-views"]')
        total_views = 0
        view_count = 0

        for element in view_elements[:20]:
            views_text = element.text
            views = format_metric(views_text)
            total_views += views
            view_count += 1

        if view_count > 0:
            profile_data['avg_views'] = total_views / view_count
        else:
            profile_data['avg_views'] = 0

    except Exception as e:
        print(f"An error occurred while scraping profile: {e}")
        return None

    finally:
        driver.quit()

    return profile_data
    

def get_video_links(profile_url: str) -> set:
    """
    Extracts the first 20 video IDs from a TikTok profile.

    Args:
        profile_url (str): The TikTok profile URL.

    Returns:
        list: A list of video IDs from the first 20 videos.
    """    
    driver = init_driver()
    video_ids = set()

    try:
        driver.get(profile_url)
        time.sleep(5)  

        videos = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/video/"]')
        
        for video in videos:
            link = video.get_attribute("href")
            video_id = link.split("/video/")[-1]
            video_ids.add(video_id)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:    
        driver.quit()

    return video_ids