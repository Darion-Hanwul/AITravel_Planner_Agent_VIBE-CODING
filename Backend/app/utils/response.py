from typing import Any, Optional
from fastapi.responses import JSONResponse
from fastapi import status

def success_response(
    data: Any = None,
    message: str = "Request berhasil diproses.",
    status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "message": message,
            "data": data
        }
    )

def error_response(
    message: str = "Terjadi kesalahan pada server.",
    errors: Optional[Any] = None,
    status_code: int = status.HTTP_400_BAD_REQUEST
) -> JSONResponse:
    content = {
        "status": "error",
        "message": message
    }
    
    if errors is not None:
        content["errors"] = errors
        
    return JSONResponse(
        status_code=status_code,
        content=content
    )