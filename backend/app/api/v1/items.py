from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc

from app.core.database import get_db
from app.models.item import PulseItem
from app.schemas.item import PulseItemCreate, PulseItemResponse, PulseItemListResponse

router = APIRouter()

@router.get("", response_model=PulseItemListResponse)
def get_items(
    category: Optional[str] = Query(None, description="Filter by category: competition, academic, etc."),
    campus: Optional[str] = Query(None, description="Filter by campus: 屯溪路, 翡翠湖, 宣城, 全部"),
    search: Optional[str] = Query(None, description="Search keyword in title, summary, or tags"),
    upcoming_only: bool = Query(False, description="Only show items with future deadline"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(PulseItem)

    if category:
        query = query.filter(PulseItem.category == category)
    if campus and campus != "全部":
        query = query.filter(or_(PulseItem.campus == campus, PulseItem.campus == "全部"))
    if upcoming_only:
        now = datetime.now()
        query = query.filter(PulseItem.deadline >= now)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                PulseItem.title.like(search_pattern),
                PulseItem.summary.like(search_pattern),
                PulseItem.tags.like(search_pattern)
            )
        )

    total = query.count()
    # Order by deadline (upcoming first if available), otherwise by publish_date desc
    items = query.order_by(
        desc(PulseItem.publish_date),
        desc(PulseItem.id)
    ).offset((page - 1) * limit).limit(limit).all()

    return {"total": total, "items": items}

@router.get("/{item_id}", response_model=PulseItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(PulseItem).filter(PulseItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Increment view count
    item.view_count += 1
    db.commit()
    db.refresh(item)
    return item

@router.post("", response_model=PulseItemResponse, status_code=201)
def create_item(payload: PulseItemCreate, db: Session = Depends(get_db)):
    existing = db.query(PulseItem).filter(PulseItem.url == payload.url).first()
    if existing:
        raise HTTPException(status_code=400, detail="Item with this URL already exists")

    item = PulseItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
