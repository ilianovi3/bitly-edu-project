from app.models import Link
from .base import BaseRepository

from sqlalchemy import select, or_, delete, func
from datetime import datetime, timezone


class LinkRepository(BaseRepository):
    async def get_all(self) -> list[Link]:
        stmt = (
            select(Link)
        )
        instances = await self._session.execute(stmt)
        results = instances.scalars().all()
        if not results:
            return []

        return [item for item in results]

    async def get_by_slug(self, slug: str) -> Link | None:
        stmt = (
            select(Link)
            .where(Link.slug == slug)
            .where(
                or_(
                    Link.expires_at.is_(None),
                    Link.expires_at > datetime.now(timezone.utc)
                )
            )
            .limit(1)
        )
        res = await self._session.execute(stmt)
        instance = res.scalar_one_or_none()
        return instance

    async def create(self, link: Link) -> Link:
        self._session.add(link)
        await self._session.flush()
        return link

    async def delete_expired(self) -> int:
        result = await self._session.execute(
            delete(Link)
            .where(
                Link.expires_at.is_not(None),
                Link.expires_at < func.now(),
            )
        )
        return result.rowcount # type: ignore[attr-defined, no-any-return]

    async def delete(self, slug: str) -> None:
        stmt = (
            delete(Link)
            .where(Link.slug == slug)
        )
        await self._session.execute(stmt)
