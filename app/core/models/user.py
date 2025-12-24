from enum import unique
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class User(Base, IntIdPkMixin):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(500), nullable=False)