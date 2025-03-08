from app.services.scrapers.hashtag_scraper import get_usernames
from app.services.scrapers.profile_scraper import get_profile_info
from app.services.scrapers.video_scraper import get_tiktok_video_data
from app.schemas.influencer import Influencer, InfluencersList
from app.utils.stats import calculate_averages
import json
import logging

logger = logging.getLogger(__name__)

def scrape_city_data(city: str) -> InfluencersList:
    """
    Scrapes TikTok data for influencers in a given city

    Args:
        city (str): Name of city to scrape data for
        
    Returns:
        list[Influencer]: List of influencer data with engagement metrics
    """

    tag_url = f"https://www.tiktok.com/tag/{city}"
    try:
        usernames = get_usernames(tag_url)
    except Exception as e:
        logger.error(f"Error getting usernames: {e}")
        return InfluencersList(influencers_list=[])
    
    if not usernames:
        return InfluencersList(influencers_list=[])
        
    influencers = []
    
    for username in usernames:
        profile_url = f"https://www.tiktok.com/@{username}"
        try:
            profile_data = get_profile_info(profile_url)
        except Exception as e:
            logger.warning(f"Error getting profile data: {e}")
            continue
        
        if not profile_data:
            continue

        metrics = {'likes': 0, 'comments': 0, 'shares': 0, 'saves': 0}
        total_videos = len(profile_data['video_ids'])
        first_urls = []

        for video_id in profile_data['video_ids']:
            video_url = f"https://www.tiktok.com/@{username}/video/{video_id}"
            try:
                video_data = get_tiktok_video_data(video_url)
            except Exception as e:
                logger.warning(f"Error getting video data: {e}")
                continue
            
            if not video_data:
                continue

            for metric in metrics:
                metrics[metric] += video_data[metric]
            
            if len(first_urls) < 3:
                first_urls.append(video_url)

        avg_metrics = calculate_averages(metrics, total_videos)
        
        influencer = Influencer(
            name=profile_data['name'],
            username=username,
            followers=profile_data['followers'],
            location=city,
            avg_views=profile_data['avg_views'],
            avg_likes=avg_metrics['avg_likes'],
            avg_comments=avg_metrics['avg_comments'],
            avg_shares=avg_metrics['avg_shares'],
            avg_saves=avg_metrics['avg_saves'],
            firsts_urls= first_urls
        )
        
        influencers.append(influencer)
        
    return InfluencersList(influencers_list=influencers)