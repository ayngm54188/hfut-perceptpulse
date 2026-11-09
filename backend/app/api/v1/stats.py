from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.item import PulseItem
from app.schemas.item import StatsSummary

router = APIRouter()

@router.get("/summary", response_model=StatsSummary)
def get_stats_summary(db: Session = Depends(get_db)):
    now = datetime.now()
    
    total = db.query(PulseItem).count()
    competition_count = db.query(PulseItem).filter(PulseItem.category == "competition").count()
    academic_count = db.query(PulseItem).filter(PulseItem.category == "academic").count()
    upcoming = db.query(PulseItem).filter(PulseItem.deadline >= now).count()

    return {
        "total_items": total,
        "competition_count": competition_count,
        "academic_count": academic_count,
        "upcoming_deadlines": upcoming
    }
