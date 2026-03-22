from app.core.events import BaseEvent
from dataclasses import dataclass


@dataclass
class AppStartupFailedEvent(BaseEvent):
    @property
    def event(self) -> str:
        return "app_startup_failed"

@dataclass
class AppStartingEvent(BaseEvent):
    @property
    def event(self) -> str:
        return "app_starting"

@dataclass
class AppReadyEvent(BaseEvent):
    @property
    def event(self) -> str:
        return "app_ready"

@dataclass
class AppStoppingEvent(BaseEvent):
    @property
    def event(self) -> str:
        return "app_stopping"

@dataclass
class AppStoppedEvent(BaseEvent):
    @property
    def event(self) -> str:
        return "app_stopped"

@dataclass
class DBConnectingEvent(BaseEvent):
    @property
    def event(self) -> str:
        return "db_connecting"

@dataclass
class DBConnectedEvent(BaseEvent):
    @property
    def event(self) -> str:
        return "db_connected"

@dataclass
class SchedulerStartingEvent(BaseEvent):
    @property
    def event(self) -> str:
        return "scheduler_starting"

@dataclass
class SchedulerReadyEvent(BaseEvent):
    @property
    def event(self) -> str:
        return "scheduler_ready"

@dataclass
class SchedulerStoppedEvent(BaseEvent):
    @property
    def event(self) -> str:
        return "scheduler_stopped"