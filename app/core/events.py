from abc import ABC, abstractmethod
from typing import Any


class BaseEvent(ABC):
    @property
    @abstractmethod
    def event(self) -> str: ...

    def as_log(self) -> dict[str, Any]:
        return dict(self.__dict__)
