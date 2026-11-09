from fastapi import APIRouter
from app.api.v1.items import router as items_router
from app.api.v1.stats import router as stats_router
from app.api.v1.crawler import router as crawler_router

api_v1_router = APIRouter()
api_v1_router.include_router(items_router, prefix="/items", tags=["Intelligence Items"])
api_v1_router.include_router(stats_router, prefix="/stats", tags=["Statistics"])
api_v1_router.include_router(crawler_router, prefix="/crawler", tags=["Perception Crawler"])
