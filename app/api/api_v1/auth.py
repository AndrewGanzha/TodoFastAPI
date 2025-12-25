from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from schemas.user import UserOut, UserRegisterIn, TokenOut, LoginIn, TokenRefreshIn
from core.config import settings
from services.auth.deps import get_current_user
from services.auth.service import login_user, refresh_access_token, register_user

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
async def register(data: UserRegisterIn, db: AsyncSession = Depends(db_helper.session_getter)):
    user = await register_user(db, data)
    return UserOut(id=user.id, email=user.email)

@router.post("/login", response_model=TokenOut)
async def login(data: LoginIn, db: AsyncSession = Depends(db_helper.session_getter)):
    tokens = await login_user(db, data)
    return tokens

@router.post("/refresh", response_model=TokenOut)
async def refresh(data: TokenRefreshIn):
    return await refresh_access_token(data.refresh_token)

@router.get("/me", response_model=UserOut)
async def me(current_user=Depends(get_current_user(settings.auth.access_secret_key))):
    return UserOut(id=current_user.id, email=current_user.email)
