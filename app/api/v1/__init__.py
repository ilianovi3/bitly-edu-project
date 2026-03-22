from fastapi import APIRouter
from .link import router as links_router

router = APIRouter(prefix="/v1")
router.include_router(links_router)

__all__ = ['router']
