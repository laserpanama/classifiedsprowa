import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Add the project root to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.backend.api import accounts, ads, schedules
from app.backend.services import scheduler_service

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Application startup...")

    mongo_url = os.getenv("MONGO_URL")
    db_name = os.getenv("DB_NAME")

    if not mongo_url or not db_name:
        logger.error("MONGO_URL and DB_NAME must be set in the environment.")
        app.mongodb_client = None
        app.mongodb = None
    else:
        app.mongodb_client = AsyncIOMotorClient(mongo_url)
        app.mongodb = app.mongodb_client[db_name]
        try:
            await app.mongodb_client.admin.command('ping')
            logger.info("MongoDB connection successful.")
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            app.mongodb_client = None
            app.mongodb = None

    if app.mongodb_client:
        scheduler_service.initialize_scheduler(app.mongodb_client)

    yield

    # Shutdown
    logger.info("Application shutdown...")
    scheduler_service.shutdown_scheduler()
    if app.mongodb_client:
        app.mongodb_client.close()
        logger.info("Disconnected from MongoDB.")

# Create the main app
app = FastAPI(title="Classifieds Pro API", lifespan=lifespan)

# Add API routers
app.include_router(accounts.router, prefix="/api")
app.include_router(ads.router, prefix="/api")
app.include_router(schedules.router, prefix="/api")

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic root endpoint
@app.get("/api")
async def root():
    return {"message": "Welcome to Classifieds Pro API"}
