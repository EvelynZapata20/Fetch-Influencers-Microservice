import logging

import redis

from app.schemas.influencer import Influencer

logger = logging.getLogger(__name__)

r = redis.Redis(host="www.tiktrack.site", port=6379, db=0, decode_responses=True)


def add_influencer(influencer: Influencer) -> None:
    """Save an influencer in a queue."""
    influencer_json = influencer.json()
    r.rpush("influencers", influencer_json)
    logger.info(f"Added influencer {influencer.username} to the queue.")


def get_influencer() -> Influencer:
    """Obtain the next influencer in the queue."""
    influencer_json = r.lpop("influencers")
    if influencer_json:
        return Influencer.parse_raw(influencer_json)
    return None
