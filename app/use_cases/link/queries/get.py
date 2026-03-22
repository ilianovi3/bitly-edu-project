from app.repositories.link import LinkRepository
from app.core.logging import get_logger
from app.schemas.link import LinkResponse

from typing import Generator
logger = get_logger(__name__)


class GetManyLinkUseCase:
    repo: LinkRepository

    def __init__(self, repo: LinkRepository):
        self.repo = repo

    async def execute(self) -> list[LinkResponse]:
        links = await self.repo.get_all()
        link_schemas = [LinkResponse.model_validate(link) for link in links]
        return link_schemas

