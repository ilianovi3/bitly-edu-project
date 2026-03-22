from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, DateTime
from datetime import datetime

from app.core.database import Base
from .base import TimestampMixin


class Link(TimestampMixin, Base):
    __tablename__ = 'links'

    slug: Mapped[str] = mapped_column(Text, primary_key=True)
    url: Mapped[str] = mapped_column(Text)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
