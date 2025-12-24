from enum import unique

from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class UserBase(Base, IntIdPkMixin):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()