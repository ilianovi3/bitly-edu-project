import uuid
import time
import structlog
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.core.logging import get_logger
from app.schemas import ErrorResponse, ErrorDetail
from .events import (
    RequestStartedEvent,
    RequestFinishedEvent,
    RequestFailedEvent
)


logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        # Привязываем к контексту.
        # ВСЕ логи в этом запросе получат эти поля автоматически.
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        logger.info(RequestStartedEvent())

        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            logger.info(
                RequestFinishedEvent(
                    status_code=response.status_code,
                    duration_ms=duration_ms
                )
            )
            response.headers["X-Request-ID"] = request_id
            return response

        except Exception:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.exception(RequestFailedEvent(duration_ms=duration_ms))

            # Middleware обязян вернуть ответ клиенту, здесь рейз - запрещён
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ErrorResponse(
                    error=ErrorDetail(
                        code="InternalServerError",
                        message="Internal server error",
                    )
                ).model_dump(),
                headers={"X-Request-ID": request_id},
            )

        finally:
            # ОБЯЗАТЕЛЬНО — иначе контекст утечёт в следующий запрос!
            structlog.contextvars.clear_contextvars()
