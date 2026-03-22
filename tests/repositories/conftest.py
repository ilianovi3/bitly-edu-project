import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.link import LinkRepository


@pytest.fixture
def repo(
    db_session: AsyncSession
) -> LinkRepository:
    return LinkRepository(session=db_session)
