from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from question_5.db.base import Base


class Country(Base):
    """Model for storing country codes."""

    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(length=2))

    def __init__(self, code: str):
        self.code = code