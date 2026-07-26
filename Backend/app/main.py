from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    auth,
    calendar,
    chat,
    history,
    rag,
    saved_place,
    tool,
    trip,
    user,
)
from app.config import settings  # Pastikan Anda memiliki konfigurasi settings di core
from app.middleware.auth import AuthenticationMiddleware
from app.middleware.logging import LoggingMiddleware

def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Travel Agent API",
        description="Backend API untuk sistem AI Travel Agent berbasis RAG dan LangChain Agent.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    origins = [
        "http://localhost:3000",  
        "http://127.0.0.1:3000",
        "*",                     
    ]
    
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(AuthenticationMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ==========================================================
    # CORS MIDDLEWARE CONFIGURATION
    # ==========================================================
    # Sesuaikan origins dengan kebutuhan frontend Anda

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(user.router)
    app.include_router(trip.router)
    app.include_router(chat.router)
    app.include_router(calendar.router)
    app.include_router(history.router)
    app.include_router(saved_place.router)
    app.include_router(tool.router)
    app.include_router(rag.router)

    @app.get("/", tags=["Health Check"], summary="Mengecek status aplikasi")
    def root():
        return {
            "status": "online",
            "message": "AI Travel Agent API is running smoothly.",
            "environment": getattr(settings, "ENVIRONMENT", "development")
        }

    return app

app = create_app()