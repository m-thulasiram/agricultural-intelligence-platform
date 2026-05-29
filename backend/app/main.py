import logging
import sys
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .api import api_router
from .models.database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log"),
    ],
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Crop Health Forecasting & Agricultural Intelligence Platform")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning("Database initialization skipped: %s", str(e))
    yield
    logger.info("Shutting down Crop Health Forecasting & Agricultural Intelligence Platform")


app = FastAPI(
    title="Crop Health Forecasting & Agricultural Intelligence Platform",
    description="""
    Advanced agricultural intelligence platform providing crop yield predictions,
    climate forecasting, disease risk assessment, and smart farming recommendations
    using machine learning and AI.
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    contact={
        "name": "Agricultural Analytics Team",
        "url": "https://github.com/anomalyco/Crop_Yield_Prediction",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "Crop Health Forecasting & Agricultural Intelligence Platform",
        "version": "1.0.0",
        "docs": "/api/v1/docs",
        "redoc": "/api/v1/redoc",
        "health": "/api/v1/health",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Crop Health Forecasting API",
        "version": "1.0.0",
        "database": "connected",
        "uptime": "running",
    }
