from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any
from app.core.database import Base, engine
from app.core.scheduler import scheduler
from app.core.readiness import readiness
from app.core.logging import setup_logging, get_logger
from .events import (
    AppStartupFailedEvent,
    AppStartingEvent,
    AppStoppingEvent,
    AppStoppedEvent,
    AppReadyEvent,
    DBConnectingEvent,
    DBConnectedEvent,
    SchedulerStartingEvent,
    SchedulerReadyEvent,
    SchedulerStoppedEvent
)


logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, Any]:
    setup_logging()
    readiness.mark_not_ready()
    logger.info(AppStartingEvent())

    try:
        logger.info(DBConnectingEvent())
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(DBConnectedEvent())

        logger.info(SchedulerStartingEvent())
        scheduler.start()
        logger.info(SchedulerReadyEvent())

        readiness.mark_ready()
        logger.info(AppReadyEvent())
    except Exception:
        logger.exception(AppStartupFailedEvent())
        readiness.mark_not_ready()
        raise

    try:
        yield
    finally:
        readiness.mark_not_ready()
        logger.info(AppStoppingEvent())
        scheduler.shutdown(wait=False)
        logger.info(SchedulerStoppedEvent())
        await engine.dispose()
        logger.info(AppStoppedEvent())
