from __future__ import annotations

import logging
import uuid
from datetime import timedelta
from typing import Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.core.security import verify_password, hash_password
from app.core.jwt import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

logger = logging.getLogger("app.api.auth")

router = APIRouter(prefix="/auth", tags=["Authentication"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:

    logger.info(f"[Auth API] Memproses pendaftaran pengguna baru dengan email: {user_in.email}")
    
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        logger.warning(f"[Auth API] Pendaftaran gagal. Email '{user_in.email}' sudah terdaftar.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ini telah digunakan oleh pengguna lain."
        )

    try:
        hashed_password = hash_password(user_in.password)
        waktu_sekarang = datetime.utcnow()

        new_user = User(
            id=str(uuid.uuid4()),
            full_name=user_in.full_name,
            email=user_in.email,
            password_hash=hashed_password,
            avatar_url=None,
            created_at=waktu_sekarang, # Wajib diisi agar PostgreSQL tidak menolak
            updated_at=waktu_sekarang  # Wajib diisi agar PostgreSQL tidak menolak
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"[Auth API] Pengguna sukses terdaftar secara legal. ID: {new_user.id}")
        return new_user
        
    except Exception as exc:
        db.rollback()
        logger.error(f"[Auth API] Gagal menyimpan user baru ke database: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Terjadi kegagalan sistem saat memproses pembuatan akun."
        )


@router.post("/signin", response_model=TokenResponse)
def signin(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
) -> Any:

    logger.info(f"[Auth API] Memproses autentikasi masuk untuk email: {form_data.username}")
    
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        logger.warning(f"[Auth API] Login gagal untuk email: {form_data.username}. Kredensial tidak cocok.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau password yang Anda masukkan salah.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # PERBAIKAN: Menyesuaikan parameter dengan tanda tangan fungsi di core/jwt.py
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires,
        additional_claims={"email": user.email}
    )

    logger.info(f"[Auth API] Login berhasil. Token berhasil diterbitkan untuk User ID: {user.id}")
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }