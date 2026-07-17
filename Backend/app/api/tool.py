from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer

from app.core.dependency import get_auth_service, get_tool_log_service
from app.core.exceptions import ResourceNotFoundError
from app.schemas.tool import ToolLogResponse
from app.services.auth_service import AuthService
from app.services.tool_log_service import ToolLogService

logger = logging.getLogger("app.api.tool")
router = APIRouter(prefix="/tools", tags=["Tool Execution Logs"])
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
            detail="Token tidak valid.",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/logs/trip/{trip_id}", response_model=list[ToolLogResponse])
def get_logs_by_trip(
    trip_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    tool_log_service: ToolLogService = Depends(get_tool_log_service),
) -> Any:
    logger.info(f"[Tool API] Mengambil log tool berdasarkan trip {trip_id}")
    return tool_log_service.get_trip_logs(trip_id=trip_id)

@router.get("/logs/filter", response_model=list[ToolLogResponse])
def get_logs_by_filter(
    tool_name: str | None = Query(default=None, description="Filter nama tool tertentu"),
    status_type: str | None = Query(default=None, enum=["success", "failed"], description="Filter status eksekusi"),
    current_user: Any = Depends(get_current_user_from_token),
    tool_log_service: ToolLogService = Depends(get_tool_log_service),
) -> Any:
    logger.info(f"[Tool API] Mengambil log tool dengan filter name={tool_name}, status={status_type}")
    
    if tool_name:
        return tool_log_service.get_tool_logs(tool_name=tool_name)
    if status_type == "success":
        return tool_log_service.get_success_logs()
    if status_type == "failed":
        return tool_log_service.get_failed_logs()
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tentukan filter 'tool_name' atau 'status_type'")

@router.get("/logs/{log_id}", response_model=ToolLogResponse)
def get_single_tool_log(
    log_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    tool_log_service: ToolLogService = Depends(get_tool_log_service),
) -> Any:
    logger.info(f"[Tool API] Mengambil log detail untuk ID: {log_id}")
    try:
        return tool_log_service.get_log(log_id=log_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))