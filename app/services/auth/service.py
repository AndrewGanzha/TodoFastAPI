from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from repository.users import (
    UserAlreadyExistsError,
    create_user,
    get_user_by_email,
)
from schemas.user import LoginIn, TokenOut, UserRegisterIn
from services.auth.jwt import create_access_token, create_refresh_token, decode_token
from services.auth.security import hash_password, verify_password


async def register_user(db: AsyncSession, data: UserRegisterIn):
    existing = await get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    try:
        return await create_user(
            db,
            email=data.email,
            username=data.username,
            password_hash=hash_password(data.password),
        )
    except UserAlreadyExistsError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err


async def login_user(db: AsyncSession, data: LoginIn) -> TokenOut:
    user = await get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return _issue_tokens_for_user(user_id=user.id)


def _issue_tokens_for_user(*, user_id: int) -> TokenOut:
    access = create_access_token(
        subject=str(user_id),
        secret_key=settings.auth.access_secret_key,
        expires_minutes=settings.auth.access_token_expire_minutes,
    )
    refresh = create_refresh_token(
        subject=str(user_id),
        secret_key=settings.auth.refresh_secret_key,
        expires_minutes=settings.auth.refresh_token_expire_minutes,
    )
    return TokenOut(access_token=access, refresh_token=refresh)


async def refresh_access_token(refresh_token: str) -> TokenOut:
    try:
        payload = decode_token(refresh_token, secret_key=settings.auth.refresh_secret_key)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject")

    try:
        user_id = int(sub)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

    return _issue_tokens_for_user(user_id=user_id)
