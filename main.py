from fastapi import FastAPI
from scraper_controller import run_spider

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Scrapy + FastApi is working"}


@app.post("/scrape/")
def start_scrape(spider_name: str):
    result = run_spider(spider_name)
    return {"status": "started", "spider":spider_name, "result": result}
