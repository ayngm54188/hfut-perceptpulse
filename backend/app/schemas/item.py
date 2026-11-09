from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class PulseItemBase(BaseModel):
    title: str
    category: str
    source_site: str
    campus: Optional[str] = "全部"
    url: str
    content_raw: Optional[str] = None
    summary: Optional[str] = None
    publish_date: Optional[date] = None
    deadline: Optional[datetime] = None
    location: Optional[str] = None
    tags: Optional[str] = None

class PulseItemCreate(PulseItemBase):
    pass

class PulseItemResponse(PulseItemBase):
    id: int
    view_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PulseItemListResponse(BaseModel):
    total: int
    items: List[PulseItemResponse]

class StatsSummary(BaseModel):
    total_items: int
    competition_count: int
    academic_count: int
    upcoming_deadlines: int
