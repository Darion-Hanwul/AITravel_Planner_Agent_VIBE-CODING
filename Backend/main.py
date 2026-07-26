from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config.cors import ALLOWED_ORIGINS
from app.config.settings import settings
from app.db.init_db import init_database
from app.db.session import engine
from app.middleware.exception import register_exception_handlers

logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Memulai {settings.APP_NAME}...")

    try:
        init_database()
        logger.info("Inisialisasi database sukses dilakukan.")
    except Exception as exc:
        logger.critical(f"Gagal melakukan inisialisasi database saat startup: {exc}")

    yield

    logger.info(f"Menghentikan {settings.APP_NAME}...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENV,
        "status": "Running",
    }


@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
    }


@app.get("/db-test", tags=["System"])
async def db_test():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()

        return {
            "status": "connected",
            "database": version
        }
    except Exception as exc:
        logger.error(f"[Main API] Gagal terhubung ke database via /db-test: {exc}")
        return {
            "status": "disconnected",
            "error": "Layanan database tidak dapat dijangkau."
        }