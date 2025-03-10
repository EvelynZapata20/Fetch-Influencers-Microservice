from fastapi import APIRouter
from app.use_cases.fetch_tiktok_data import fetch_influencers_by_tag
from app.schemas.influencer import InfluencersList

router = APIRouter()

@router.get("/api/v1/influencers/{city}", response_model=InfluencersList)
def get_influencers(city: str):
    return fetch_influencers_by_tag(city)