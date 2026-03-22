from .base import TimestampSchema
from app.core.config import get_settings

from pydantic import BaseModel, HttpUrl, AfterValidator, Field
from app.core.exceptions import UrlIsTooLong

from datetime import datetime
from typing import Annotated


settings = get_settings()


def check_url_length(url: HttpUrl) -> HttpUrl:
    if settings.URL_MAX_LENGTH is None:
        return url

    if len(str(url)) > settings.URL_MAX_LENGTH:
        raise UrlIsTooLong()
    return url

ValidUrl = Annotated[HttpUrl, AfterValidator(check_url_length)]


class LinkCreate(BaseModel):
    url: ValidUrl
    expire_in: int | None = Field(
        default=None,
        gt=settings.SLUG_EXPIRY_MIN_SECONDS,
        lt=settings.SLUG_EXPIRY_MAX_SECONDS
    )
    custom_slug: str | None = Field(
        default=None,
        min_length=settings.CUSTOM_SLUG_MIN_LENGTH,
        max_length=settings.CUSTOM_SLUG_MAX_LENGTH,
        pattern=settings.CUSTOM_SLUG_PATTERN
    )

class LinkResponse(TimestampSchema):
    slug: str
    url: str
    expires_at: datetime | None
