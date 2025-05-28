from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.routes import router
from app.use_cases.fetch_tiktok_data import fetch_influencers_by_tag
from app.utils.web_driver import WebDriverManager

app = FastAPI(title="TikTok Scraper API", version="1.0")

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


driver = WebDriverManager.get_driver()

scheduler = BackgroundScheduler()
scheduler.add_job(
    fetch_influencers_by_tag, "interval", minutes=20, next_run_time=datetime.now()
)
scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

