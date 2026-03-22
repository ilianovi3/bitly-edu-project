from dataclasses import dataclass
from app.core.events import BaseEvent
from datetime import datetime


@dataclass
class SlugCreatedEvent(BaseEvent):
    slug: str
    url: str
    custom: bool
    expires_at: datetime | None

    @property
    def event (self) -> str:
        return "slug_created"

@dataclass
class SlugResolvedEvent(BaseEvent):
    slug: str
    url: str

    @property
    def event(self) -> str:
        return "slug_resolved"


@dataclass
class SlugNotFoundEvent(BaseEvent):
    slug: str

    @property
    def event(self) -> str:
        return "slug_not_found"


@dataclass
class SlugAlreadyExistsEvent(BaseEvent):
    slug: str

    @property
    def event(self) -> str:
        return "slug_already_exists"