from fastapi import FastAPI
from app.routes.routes import router
from app.utils.web_driver import WebDriverManager

app = FastAPI(title="TikTok Scraper API", version="1.0")

app.include_router(router)

driver = WebDriverManager.get_driver()


@app.get("/")
def root():
    return {"message": "API is running!"}