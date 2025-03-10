from pydantic import BaseModel

class Influencer(BaseModel):
    """
    Schema for a TikTok influencer with engagement metrics from their last 10 videos.

    Attributes:
        username (str): The TikTok username.
        profile_name (str): The influencer's full name.
        profile_picture (str): The URL of the influencer's profile image.
        profile_url (str): The URL of the influencer's profile.
        average_likes (float): Average number of likes on the last 10 videos.
        average_comments (float): Average number of comments on the last 10 videos.
        average_shares (float): Average number of shares on the last 10 videos.
        average_saves (float): Average number of saves on the last 10 videos.
        average_views (float): Average number of views on the last 10 videos.
        followers (int): Total number of followers.
        city (str): The influencer's location, determined by the scraped tag.
        featured_videos (list[str]): List of URLs of the first 3 videos.
    """
    username: str
    profile_name: str
    profile_picture: str
    profile_url: str
    average_likes: float
    average_comments: float
    average_shares: float
    average_saves: float
    average_views: float
    followers: int
    city: str 
    featured_videos: list[str]

    @property
    def engagement_visualization_rate(self) -> float:
        """Returns the engagement-to-view ratio for an influencer."""
        total_engagement = self.average_likes + self.average_comments + self.average_shares + self.average_saves
        return total_engagement / self.average_views if self.average_views > 0 else 0

    def is_significant(self) -> bool:
        """
        Determine if an influencer meets the criteria to be considered significant.
        """
        
        min_engagement_per_type = {
            "micro": 0.05,
            "macro": 0.03,
            "mega": 0.02,
            "celebrity": 0.01
        }
        
        if self.followers <= 10000:
            return False
        elif self.followers <= 100000:
            return self.engagement_visualization_rate >= min_engagement_per_type["micro"]
        elif self.followers <= 1000000:
            return self.engagement_visualization_rate >= min_engagement_per_type["macro"]
        elif self.followers <= 10000000:
            return self.engagement_visualization_rate >= min_engagement_per_type["mega"]
        elif self.followers <= 10000000:
            return self.engagement_visualization_rate >= min_engagement_per_type["celebrity"]
        else:
            return True
    
    
class InfluencersList(BaseModel):
    """
    Schema for a list of influencers.
    """

    influencers_list: list[Influencer]

