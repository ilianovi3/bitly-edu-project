from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from app.core.database import AsyncSessionMaker

from app.services.link.generator import SlugGenerator
from app.repositories.link import LinkRepository

from app.use_cases.link import RedirectLinkUseCase, GetManyLinkUseCase, CreateLinkUseCase, DeleteLinkUseCase


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_create_link_use_case(
    db: AsyncSession = Depends(get_db),
) -> CreateLinkUseCase:
    return CreateLinkUseCase(
        repo=LinkRepository(db),
        slug_generator=SlugGenerator(),
    )

async def get_delete_link_use_case(
    db: AsyncSession = Depends(get_db),
) -> DeleteLinkUseCase:
    return DeleteLinkUseCase(
        repo=LinkRepository(db),
    )


async def get_redirect_link_use_case(
    db: AsyncSession = Depends(get_db),
) -> RedirectLinkUseCase:
    return RedirectLinkUseCase(
        repo=LinkRepository(db)
    )

async def get_many_link_use_case(
    db: AsyncSession = Depends(get_db),
) -> GetManyLinkUseCase:
    return GetManyLinkUseCase(
        repo=LinkRepository(db)
    )