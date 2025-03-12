from app.databases.redis import get_influencer
from app.schemas.influencer import InfluencersList
from app.utils.case_converter import influencers_to_camel
def retrive_tiktok_influencers()-> InfluencersList:
    influencers = []
    while(True):
        influencer = get_influencer()
        if not influencer:
            break
        influencers.append(influencer)

    camel_influencers = influencers_to_camel(influencers)
    return camel_influencers