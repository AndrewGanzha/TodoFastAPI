from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from repository.users import get_user_by_id
from services.auth.jwt import decode_token


def get_token_from_header(authorization: str | None = Header(default=None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise HTTPException(status_code=401, detail="Invalid auth scheme")
    return authorization[len(prefix):].strip()

def get_current_user(secret_key: str):
    async def _dep(
        db: AsyncSession = Depends(db_helper.session_getter),
        token: str = Depends(get_token_from_header),
    ) -> User:
        try:
            payload = decode_token(token, secret_key=secret_key)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Token missing subject")

        try:
            user_id = int(sub)
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid token subject")

        user = await get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    return _dep
