from fastapi import APIRouter
from app.schemas.influencer import InfluencersList
from app.use_cases.retrieve_tiktok_influencers import retrive_tiktok_influencers

router = APIRouter()

@router.get("/api/v1/influencers", response_model=InfluencersList)
def get_influencers() -> InfluencersList:  
    return retrive_tiktok_influencers()