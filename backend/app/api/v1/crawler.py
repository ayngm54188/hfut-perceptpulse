from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.crawlers.manager import CrawlerManager

router = APIRouter()

@router.post("/run")
def trigger_crawler(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Trigger real-time crawling of HFUT campus websites.
    """
    manager = CrawlerManager(db=db)
    result = manager.run_all()
    return result
