from typing import Awaitable, Callable

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from repository.users import get_user_by_id
from services.auth.jwt import decode_token


bearer_scheme = HTTPBearer(auto_error=True)


def get_token_from_header(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> str:
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")
    return credentials.credentials

def get_current_user(secret_key: str) -> Callable[..., Awaitable[User]]:
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
