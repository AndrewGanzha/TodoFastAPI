from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models.todo import Todo


class User(Base, IntIdPkMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(500), nullable=False)
    todos: Mapped[list["Todo"]] = relationship(
        "Todo",
        back_populates="user",
        cascade="all, delete-orphan",
    )
