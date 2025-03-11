from fastapi import FastAPI
from app.routes.routes import router
from app.utils.web_driver import WebDriverManager
from apscheduler.schedulers.background import BackgroundScheduler
from app.use_cases.fetch_tiktok_data import fetch_influencers_by_tag
from datetime import datetime

app = FastAPI(title="TikTok Scraper API", version="1.0")
app.include_router(router)

driver = WebDriverManager.get_driver()

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_influencers_by_tag, "interval", hours=24, next_run_time=datetime.now())
scheduler.start()

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

@app.get("/")
def root():
    return {"message": "API is running!"}