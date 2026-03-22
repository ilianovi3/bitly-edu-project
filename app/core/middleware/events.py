from app.core.events import BaseEvent
from dataclasses import dataclass


@dataclass
class RequestStartedEvent(BaseEvent):
    @property
    def event(self) -> str:
        return "request_started"

@dataclass
class RequestFinishedEvent(BaseEvent):
    status_code: int
    duration_ms: float

    @property
    def event(self) -> str:
        return "request_finished"

@dataclass
class RequestFailedEvent(BaseEvent):
    duration_ms: float

    @property
    def event(self) -> str:
        return "request_failed"