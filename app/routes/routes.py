from fastapi import APIRouter

from app.use_cases.retrieve_tiktok_influencers import retrive_tiktok_influencers
from app.use_cases.send_message_to_influencer import send_message_to_influencer
from pydantic import BaseModel
from fastapi import HTTPException

class MessagePayload(BaseModel):
    message: str

router = APIRouter()

@router.get("/")
def root():
    return {"message": "API is running!"}

@router.get("/api/v1/influencers")
def get_influencers():
    return retrive_tiktok_influencers()

@router.post("/api/v1/messages/{username}")
async def send_message(username: str, payload: MessagePayload):
    if not payload.message:
        raise HTTPException(status_code=400, detail="Message is required")

    try:
        success = send_message_to_influencer(username, payload.message)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send message")
        return {"status": "success", "message": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))