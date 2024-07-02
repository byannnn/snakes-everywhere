from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from question_5.db.base import Base


class User(Base):
    """User model for storing authentication information."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
    password: Mapped[str] = mapped_column(String(length=200))
    salt: Mapped[str] = mapped_column(String(length=200))

    def __init__(self, name: str, password: str, salt: str):
        self.name = name
        self.password = password
        self.salt = salt
