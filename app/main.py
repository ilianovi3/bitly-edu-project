from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.api import router as api_router
from app.core.exceptions import AppException
from app.core.config import get_settings
from app.core.middleware import LoggingMiddleware
from app.core.lifespan import lifespan
from app.core.exception_handlers import app_exception_handler, validation_exception_handler


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    debug=settings.IS_DEV,
    docs_url="/docs" if settings.IS_DEV else None,
    openapi_url="/openapi.json" if settings.IS_DEV else None,
    redoc_url=None,
)
app.add_middleware(LoggingMiddleware)
app.include_router(api_router)
app.exception_handler(AppException)(app_exception_handler)
app.exception_handler(RequestValidationError)(validation_exception_handler)
