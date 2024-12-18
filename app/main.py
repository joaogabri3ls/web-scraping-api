from fastapi import FastAPI
from app.endpoints import news

app = FastAPI(title="Web Scraping API")

app.include_router(news.router, prefix="/api/v1", tags=["news"])

@app.get("/", summary="Root Endpoint")
async def root():
    return {"message": "Web Scraping API is running!"}
