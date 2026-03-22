import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.link import LinkRepository
from app.models.link import Link
from datetime import datetime, timezone, timedelta


@pytest.mark.parametrize("slug,has_expiry", [
    ("slug-1", False),
    ("slug-2", True)
])
async def test_create_link(
    repo: LinkRepository,
    slug: str,
    has_expiry: bool
) -> None:
    expires_at = datetime.now(timezone.utc) if has_expiry else None
    link = Link(url="https://domain.com", slug=slug, expires_at=expires_at)
    created = await repo.create(link)
    assert created.slug == slug


@pytest.fixture
async def created_link(
    db_session: AsyncSession,
) -> Link:
    link = Link(url="https://example.com", slug="created-link")
    db_session.add(link)
    await db_session.commit()
    return link


@pytest.fixture
async def expired_created_link(
    db_session: AsyncSession,
) -> Link:
    expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    link = Link(url="https://example.com", slug="created-link-expired", expires_at=expires_at)
    db_session.add(link)
    await db_session.commit()
    return link


async def test_get_by_slug_returns_link(
    repo: LinkRepository,
    created_link: Link
) -> None:
    result = await repo.get_by_slug(created_link.slug)

    assert result is not None
    assert result.slug == created_link.slug
    assert result.url == created_link.url
    assert result.expires_at == created_link.expires_at


async def test_get_by_slug_returns_none_when_missing(
    repo: LinkRepository,
) -> None:
    result = await repo.get_by_slug("nonexistent")
    assert result is None


async def test_delete_by_slug(
    repo: LinkRepository,
    created_link: Link
) -> None:
    await repo.delete(created_link.slug)
    result = await repo.get_by_slug(created_link.slug)
    assert result is None


async def test_delete_expired_links(
    repo: LinkRepository,
    expired_created_link: Link
) -> None:
    count = await repo.delete_expired()
    assert count == 1
