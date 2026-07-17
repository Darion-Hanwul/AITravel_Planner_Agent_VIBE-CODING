from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer

from app.core.dependency import get_auth_service, get_document_service
from app.core.exceptions import DocumentNotFoundError
from app.schemas.document import DocumentBase, DocumentResponse
from app.services.auth_service import AuthService
from app.services.document_service import DocumentService

logger = logging.getLogger("app.api.rag")
router = APIRouter(prefix="/rag/documents", tags=["RAG Documents"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")

def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    try:
        return auth_service.verify_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Otorisasi gagal.",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document_metadata(
    data: DocumentBase,
    current_user: Any = Depends(get_current_user_from_token),
    document_service: DocumentService = Depends(get_document_service),
) -> Any:
    logger.info(f"[RAG API] Menambahkan metadata dokumen baru: {data.title}")
    return document_service.create_document(data=data)

@router.get("", response_model=list[DocumentResponse])
def list_all_documents(
    current_user: Any = Depends(get_current_user_from_token),
    document_service: DocumentService = Depends(get_document_service),
) -> Any:
    logger.info("[RAG API] Mengambil daftar seluruh dokumen pengetahuan")
    return document_service.get_documents()

@router.get("/search", response_model=DocumentResponse)
def search_document_by_title(
    title: str = Query(..., description="Judul dokumen yang dicari tepat"),
    current_user: Any = Depends(get_current_user_from_token),
    document_service: DocumentService = Depends(get_document_service),
) -> Any:
    logger.info(f"[RAG API] Mencari dokumen dengan judul: {title}")
    document = document_service.search_by_title(title=title)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dokumen tidak ditemukan.")
    return document

@router.get("/source", response_model=list[DocumentResponse])
def get_documents_by_source(
    source: str = Query(..., description="Sumber asal dokumen"),
    current_user: Any = Depends(get_current_user_from_token),
    document_service: DocumentService = Depends(get_document_service),
) -> Any:
    logger.info(f"[RAG API] Memfilter dokumen berdasarkan asal: {source}")
    return document_service.get_by_source(source=source)

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document_detail(
    document_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    document_service: DocumentService = Depends(get_document_service),
) -> Any:
    logger.info(f"[RAG API] Mengambil detail dokumen ID: {document_id}")
    try:
        return document_service.get_document(document_id=document_id)
    except DocumentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    document_service: DocumentService = Depends(get_document_service),
) -> None:
    logger.info(f"[RAG API] Menghapus dokumen ID: {document_id}")
    try:
        document_service.delete_document(document_id=document_id)
    except DocumentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))