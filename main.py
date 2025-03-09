from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI(title="TikTok Scraper API", version="1.0")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "API is running!"}