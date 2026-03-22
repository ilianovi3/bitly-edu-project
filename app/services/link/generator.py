from app.core.config import get_settings
import random

settings = get_settings()

class SlugGenerator:
    def __init__(
        self,
        length: int = settings.RANDOM_SLUG_LENGTH,
        charset: str = settings.RANDOM_SLUG_CHARSET
    ):
        self._length = length
        self._charset = charset

    def generate(self) -> str:
        return ''.join(random.choices(self._charset, k=self._length))