from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.core.readiness import readiness

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready() -> JSONResponse:
    if not readiness.is_ready:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "starting"}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "ok"}
    )
