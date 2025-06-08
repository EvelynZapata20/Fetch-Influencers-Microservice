import logging

from app.utils.get_influencer_information import get_influencer_information

logger = logging.getLogger(__name__)

def update_tiktok_influencer(username: str):
    influencer = get_influencer_information(username)
    if not influencer:
        logger.warning(f"Failed to retrieve information for {username}")
        return None
    return influencer
