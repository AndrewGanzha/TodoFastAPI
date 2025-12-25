from typing import Optional

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.models import User


class UserAlreadyExistsError(Exception):
    pass


async def get_user_by_email(db: AsyncSession, email: EmailStr) -> Optional[User]:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    return await db.get(User, user_id)

async def create_user(db: AsyncSession, *, email: EmailStr, username: str, password_hash: str) -> User:
    user = User(email=str(email), username=username, password_hash=password_hash)
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as err:
        await db.rollback()
        raise UserAlreadyExistsError("User with this email or username already exists") from err
    await db.refresh(user)
    return user
