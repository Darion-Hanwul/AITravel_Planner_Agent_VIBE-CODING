from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.middleware.exception import register_exception_handlers

from app.config.cors import ALLOWED_ORIGINS
from app.config.settings import settings
from app.db.init_db import init_database
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting TravelPlannerAgent...")

    # Test koneksi database saat startup
    init_database()

    yield

    print("Stopping TravelPlannerAgent...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app = FastAPI()

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENV,
        "status": "Running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
    }


@app.get("/db-test")
def db_test():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.scalar()

    return {
        "database": version
    }