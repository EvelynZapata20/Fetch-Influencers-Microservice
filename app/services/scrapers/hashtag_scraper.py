from app.utils.web_driver import WebDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import re
import random
import logging
logger = logging.getLogger(__name__)

def get_usernames(url_hashtag: str) -> set:
    driver = WebDriverManager.get_driver()
    usernames = set()

    try:
        driver.get(url_hashtag)
        wait = WebDriverWait(driver, random.uniform(8, 12))
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="search_video-item"]')))
        
        for _ in range(10):  
            driver.execute_script("window.scrollBy(0, 2000);")
            time.sleep(random.uniform(1.5, 3.5))

        videos = driver.find_elements(By.CSS_SELECTOR, '[data-e2e="search_video-item"]')
        for video in videos:
            try:
                link_element = video.find_element(By.TAG_NAME, "a")
                video_url = link_element.get_attribute("href")
                
                match = re.search(r"@([^/]+)/video", video_url)
                username = match.group(1) if match else ""
                usernames.add(username)
            except NoSuchElementException:
                continue

    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error in hashtag module: {e}")
        return None

    return usernames
