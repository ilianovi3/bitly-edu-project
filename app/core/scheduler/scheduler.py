from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.database import AsyncSessionMaker
from app.core.logging import get_logger
from app.core.config import get_settings
from app.repositories.link import LinkRepository
from .events import DeleteExpiredLinksEvent


settings = get_settings()
logger = get_logger(__name__)

async def delete_expired_links() -> None:
    async with AsyncSessionMaker() as session:
        try:
            repo = LinkRepository(session)
            count = await repo.delete_expired()
            logger.info(DeleteExpiredLinksEvent(count=count))
            await session.commit()
        except Exception:
            await session.rollback()
            raise


scheduler = AsyncIOScheduler()
scheduler.add_job(
    delete_expired_links,
    trigger="interval",
    minutes=settings.SCHEDULER_DELETE_EXPIRED_LINKS_INTERVAL_MINUTES,
    id="expired-links-cleanup",
    replace_existing=True,
)