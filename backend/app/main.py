from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import PROJECT_NAME, API_V1_STR
from app.core.database import engine, Base
from app.api.v1 import api_v1_router
# Ensure all models are imported so Base.metadata knows about them
import app.models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables are created in SQLite
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=PROJECT_NAME,
    description="HFUT-PerceptPulse 校园学术与竞赛情报感知系统 API",
    version="0.1.0",
    lifespan=lifespan
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(api_v1_router, prefix=API_V1_STR)

@app.get("/")
def root():
    return {
        "status": "online",
        "system": PROJECT_NAME,
        "docs_url": "/docs",
        "version": "0.1.0"
    }
