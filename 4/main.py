from fastapi import FastAPI, BackgroundTasks

from database import SessionLocal, AnimeModel, init_db
from DataHarvest import ShikimoriParser

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/parse")
def run_parser(url: str, background_tasks: BackgroundTasks):
    db = SessionLocal()
    parser = ShikimoriParser(db)
    
    background_tasks.add_task(parser.parse, url)
    
    return {"message": "Parsing started", "url": url}

@app.get("/data")
def get_all_data():
    db = SessionLocal()
    try:
        results = db.query(AnimeModel).all()
    finally:
        db.close()
    return results