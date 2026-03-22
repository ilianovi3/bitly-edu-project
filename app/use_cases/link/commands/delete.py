from app.repositories.link import LinkRepository
from app.core.logging import get_logger


logger = get_logger(__name__)


class DeleteLinkUseCase:
    repo: LinkRepository

    def __init__(self, repo: LinkRepository):
        self.repo = repo

    async def execute(self, slug: str) -> None:
        await self.repo.delete(slug)
