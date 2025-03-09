from pydantic import BaseModel

class Influencer(BaseModel):
    """
    Schema for a TikTok influencer with engagement metrics from their last 20 videos.

    Attributes:
        name (str): The influencer's full name.
        username (str): The TikTok username.
        image_url (str): The URL of the influencer's profile image.
        followers (int): Total number of followers.
        location (str): The influencer's location, determined by the scraped tag.
        avg_likes (float): Average number of likes on the last 20 videos.
        avg_comments (float): Average number of comments on the last 20 videos.
        avg_shares (float): Average number of shares on the last 20 videos.
        avg_saves (float): Average number of saves on the last 20 videos.
        avg_views (float): Average number of views on the last 20 videos.
        firsts_urls (list[str]): List of URLs of the first 3 videos.
    """
    name: str
    username: str
    image_url: str
    followers: int
    location: str 
    avg_likes: float
    avg_comments: float
    avg_shares: float
    avg_saves: float
    avg_views: float
    firsts_urls: list[str]

class InfluencersList(BaseModel):
    """
    Schema for a list of influencers.
    """
    influencers_list: list[Influencer]

