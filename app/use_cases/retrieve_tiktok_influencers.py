from app.databases.redis import get_influencer
from app.schemas.influencer import InfluencersList

def retrive_tiktok_influencers()-> InfluencersList:
    influencers = []
    while(True):
        influencer = get_influencer()
        if not influencer:
            break
        influencers.append(influencer)
    return InfluencersList(influencers_list=influencers)