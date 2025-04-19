from fastapi import APIRouter

from app.use_cases.retrieve_tiktok_influencers import retrive_tiktok_influencers
from app.use_cases.send_message_to_influencer import send_message_to_influencer

router = APIRouter()


@router.get("/api/v1/influencers")
def get_influencers():
    return retrive_tiktok_influencers()

@router.post("/api/v1/messages/{username}/{message}")
def send_message(username: str, message: str):
    return send_message_to_influencer(username, message)