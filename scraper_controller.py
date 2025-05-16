import subprocess
from pathlib import Path

def run_spider(spider_name):
    project_dir = Path(__file__).resolve().parent / "detchie_scraper/detchie_scraper"
    print(project_dir)
    result = subprocess.run(
        ["scrapy", "crawl", spider_name],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return {"status": "success", "output": result.stdout}
    else:
        return {"status": "error", "error": result.stderr}