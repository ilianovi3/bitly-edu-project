from app.core.events import BaseEvent
from dataclasses import dataclass


@dataclass
class DeleteExpiredLinksEvent(BaseEvent):
    count: int

    @property
    def event(self) -> str:
        return "scheduler_expired_links_delete"