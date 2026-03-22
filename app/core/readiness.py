from dataclasses import dataclass, field


@dataclass
class ReadinessState:
    """Хранит состояние готовности приложения"""
    _ready: bool = field(default=False, init=False)

    def mark_ready(self) -> None:
        self._ready = True

    def mark_not_ready(self) -> None:
        self._ready = False

    @property
    def is_ready(self) -> bool:
        return self._ready


# Singleton — один объект на весь процесс
readiness = ReadinessState()
