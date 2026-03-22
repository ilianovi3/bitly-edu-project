from app.repositories.link import LinkRepository
from app.schemas.link import LinkCreate, LinkResponse
from app.models.link import Link
from app.core.logging import get_logger
from app.core.exceptions import SlugExistsError
from app.use_cases.link.events import (
    SlugCreatedEvent,
    SlugAlreadyExistsEvent,
)
from datetime import datetime, timezone, timedelta
from app.services.link.generator import SlugGenerator


logger = get_logger(__name__)


class CreateLinkUseCase:
    repo: LinkRepository
    slug_generator: SlugGenerator

    def __init__(self, repo: LinkRepository, slug_generator: SlugGenerator):
        self.repo = repo
        self.slug_generator = slug_generator

    async def execute(self, data: LinkCreate) -> LinkResponse:
        url = str(data.url)
        custom_slug = data.custom_slug
        expire_in = data.expire_in

        if isinstance(custom_slug, str):
            slug = await self._resolve_custom_slug(custom_slug=custom_slug)
        else:
            slug = self.slug_generator.generate()

        expires_at = self._resolve_expiry(expire_in=expire_in)

        instance = Link(
            slug=slug,
            url=url,
            expires_at=expires_at
        )
        link = await self.repo.create(instance)
        logger.info(SlugCreatedEvent(
            slug=slug,
            url=url,
            custom=isinstance(custom_slug, str),
            expires_at=expires_at
        ))
        return LinkResponse.model_validate(link)

    async def _resolve_custom_slug(self, custom_slug: str) -> str:
        instance = await self.repo.get_by_slug(custom_slug)
        if instance:
            logger.info(SlugAlreadyExistsEvent(slug=custom_slug))
            raise SlugExistsError()
        return custom_slug

    @staticmethod
    def _resolve_expiry(expire_in: int | None = None) -> datetime | None:
        if isinstance(expire_in, int) and expire_in > 0:
            return datetime.now(timezone.utc) + timedelta(seconds=expire_in)
        return None
