from app.services.scrapers.hashtag_scraper import get_usernames
from app.services.scrapers.profile_scraper import get_profile_info
from app.services.scrapers.video_scraper import get_tiktok_video_data
from app.schemas.influencer import Influencer, InfluencersList
from app.utils.stats import calculate_averages
import json
import logging
import random
logger = logging.getLogger(__name__)

def fetch_influencers_by_tag(city: str) -> InfluencersList:
    """
    Scrapes TikTok data for influencers in a given city

    Args:
        city (str): Name of city to scrape data for
        
    Returns:
        list[Influencer]: List of influencer data with engagement metrics
    """

    tag_url = f"https://www.tiktok.com/search/video?q={city}"
    try:
        temp_usernames = list(get_usernames(tag_url))
        count_users = 0
        usernames = []

        while(count_users < 5):
            usernames.append(temp_usernames.pop(random.randint(0, len(temp_usernames) - 1)))
            count_users += 1
        

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
        featured_videos = []

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
            
            if len(featured_videos) < 3:
                featured_videos.append(video_url)

        average_metrics = calculate_averages(metrics, total_videos)
        
        influencer = Influencer(
            username=username,
            profile_name=profile_data['profile_name'],
            profile_picture=profile_data['profile_picture'],
            profile_url=profile_url,
            average_views=profile_data['average_views'],
            average_likes=average_metrics['average_likes'],
            average_comments=average_metrics['average_comments'],
            average_shares=average_metrics['average_shares'],
            average_saves=average_metrics['average_saves'],
            followers=profile_data['followers'],
            city=city,
            featured_videos=featured_videos
        )

        if influencer.is_significant():
            influencers.append(influencer)
        
    return InfluencersList(influencers_list=influencers)