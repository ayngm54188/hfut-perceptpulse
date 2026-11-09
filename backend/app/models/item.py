from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Date
from app.core.database import Base

class PulseItem(Base):
    """
    Core table for campus intelligence items (academic lectures, competitions, etc.)
    """
    __tablename__ = "pulse_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    category = Column(String(32), nullable=False, index=True) # competition, academic, notice, scholarship
    source_site = Column(String(64), nullable=False, index=True) # e.g. 计算机与信息学院, 本科生院, 宣校管委会
    campus = Column(String(32), default="全部", index=True) # 翡翠湖, 屯溪路, 宣城, 全部, 线上
    url = Column(String(512), unique=True, nullable=False) # deduplication key
    content_raw = Column(Text, nullable=True) # full text
    summary = Column(Text, nullable=True) # brief overview
    publish_date = Column(Date, nullable=True, index=True)
    deadline = Column(DateTime, nullable=True, index=True) # registration deadline or lecture time
    location = Column(String(128), nullable=True) # e.g. 科教楼A座大报告厅, 腾讯会议
    tags = Column(String(255), nullable=True) # comma-separated tags
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class CrawlSource(Base):
    """
    Source configuration table for monitored campus websites
    """
    __tablename__ = "crawl_sources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    base_url = Column(String(512), nullable=False)
    category_default = Column(String(32), default="academic")
    is_active = Column(Boolean, default=True)
    last_crawled_at = Column(DateTime, nullable=True)
