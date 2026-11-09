from fastapi import APIRouter
from app.api.v1.items import router as items_router
from app.api.v1.stats import router as stats_router

api_v1_router = APIRouter()
api_v1_router.include_router(items_router, prefix="/items", tags=["Intelligence Items"])
api_v1_router.include_router(stats_router, prefix="/stats", tags=["Statistics"])
