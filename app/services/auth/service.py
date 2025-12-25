from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repository.users import create_user, get_user_by_email
from schemas.user import LoginIn, UserRegisterIn
from services.auth.jwt import create_access_token
from services.auth.security import hash_password, verify_password

# TODO заменить на использование env
SECRET_KEY = "CHANGE_ME"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def register_user(db: AsyncSession, data: UserRegisterIn):
    existing = await get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    return await create_user(
        db,
        email=data.email,
        username=data.username,
        password_hash=hash_password(data.password),
    )


async def login_user(db: AsyncSession, data: LoginIn) -> str:
    user = await get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return create_access_token(
        subject=str(user.id),
        secret_key=SECRET_KEY,
        expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
