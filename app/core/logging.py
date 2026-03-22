import logging
import structlog
from app.core.events import BaseEvent
from app.core.config import get_settings
from typing import Any


settings = get_settings()

def setup_logging() -> None:
    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG if settings.IS_DEV else logging.INFO,
    )
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    renderer: structlog.types.Processor = (
        structlog.dev.ConsoleRenderer(colors=True)
        if settings.IS_DEV
        else structlog.processors.JSONRenderer()
    )

    structlog.configure(
        processors=shared_processors + [renderer],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if settings.IS_DEV else logging.INFO
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


class AppLogger:
    def __init__(self, logger: structlog.stdlib.BoundLogger):
        self._logger = logger

    @staticmethod
    def _resolve(event: str | BaseEvent) -> tuple[str, dict[str, Any]]:
        if isinstance(event, BaseEvent):
            return event.event, event.as_log()
        return event, {}

    def info(self, event: str | BaseEvent, **kwargs: Any) -> None:
        name, fields = self._resolve(event)
        self._logger.info(name, **{**fields, **kwargs})

    def warning(self, event: str | BaseEvent, **kwargs: Any) -> None:
        name, fields = self._resolve(event)
        self._logger.warning(name, **{**fields, **kwargs})

    def error(self, event: str | BaseEvent, **kwargs: Any) -> None:
        name, fields = self._resolve(event)
        self._logger.error(name, **{**fields, **kwargs})

    def debug(self, event: str | BaseEvent, **kwargs: Any) -> None:
        name, fields = self._resolve(event)
        self._logger.debug(name, **{**fields, **kwargs})

    def exception(self, event: str | BaseEvent, **kwargs: Any) -> None:
        name, fields = self._resolve(event)
        self._logger.exception(name, **{**fields, **kwargs})


def get_logger(name: str = __name__) -> AppLogger:
    return AppLogger(structlog.get_logger(name))

