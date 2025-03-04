"""
TikTok Username Scraper

This script automates the extraction of unique usernames from videos 
under a TikTok hashtag page using Selenium
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_usernames(url):
    """
    Scrapes TikTok to extract unique usernames from a hashtag page.
    
    Args:
        url (str): The TikTok ag URL to scrape.
    
    Returns:
        set: A set of unique usernames found on the page.
    """

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("--log-level=3") 
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    usernames = set()

    try:
        driver.get(url)
        time.sleep(5)

        videos = driver.find_elements(By.CSS_SELECTOR, '[data-e2e="challenge-item"]')

        for video in videos:
            username = video.find_element(By.CSS_SELECTOR, '[data-e2e="challenge-item-username"]').text
            usernames.add(username)

    except Exception as e:
        print(f"An error occurred: {e}")
        

    finally:    
        driver.quit()
    
    return usernames