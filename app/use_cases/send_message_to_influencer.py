from app.services.messages.send_messages import send_message

def send_message_to_influencer(username: str, message: str) -> bool:
    """
    Sends a message to a TikTok influencer.
    
    Args:
        username (str): The TikTok username of the influencer.
        message (str): The message to send to the influencer.

    Returns:
        bool: True if message was sent successfully, False otherwise.
    """ 

    profile_url = f"https://www.tiktok.com/@{username}"
    return send_message(profile_url, message)

