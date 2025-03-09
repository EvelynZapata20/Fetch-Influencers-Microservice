from fastapi import APIRouter
from app.use_cases.scraper import scrape_city_data
from app.schemas.influencer import InfluencersList

router = APIRouter()

@router.get("/scrape/{city}", response_model=InfluencersList)
def scrape(city: str):
    return scrape_city_data(city)