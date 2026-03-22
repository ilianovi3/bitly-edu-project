from app.repositories.link import LinkRepository
from app.core.logging import get_logger
from app.core.exceptions import SlugNotFoundError
from app.use_cases.link.events import (
    SlugResolvedEvent,
    SlugNotFoundEvent
)

logger = get_logger(__name__)


class RedirectLinkUseCase:
    repo: LinkRepository

    def __init__(self, repo: LinkRepository):
        self.repo = repo

    async def execute(self, slug: str) -> str:
        instance = await self.repo.get_by_slug(slug)
        if not instance:
            logger.warning(SlugNotFoundEvent(slug=slug))
            raise SlugNotFoundError()
        url = instance.url
        logger.info(SlugResolvedEvent(slug=slug, url=url))
        return url