from sqlalchemy.orm import DeclarativeBase

from question_5.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
