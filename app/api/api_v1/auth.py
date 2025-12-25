from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from schemas.user import UserOut, UserRegisterIn, TokenOut, LoginIn
from core.config import settings
from services.auth.deps import get_current_user
from services.auth.service import login_user, register_user

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
async def register(data: UserRegisterIn, db: AsyncSession = Depends(db_helper.session_getter)):
    user = await register_user(db, data)
    return UserOut(id=user.id, email=user.email)

@router.post("/login", response_model=TokenOut)
async def login(data: LoginIn, db: AsyncSession = Depends(db_helper.session_getter)):
    token = await login_user(db, data)
    return TokenOut(access_token=token)

@router.get("/me", response_model=UserOut)
async def me(current_user=Depends(get_current_user(settings.auth.access_secret_key))):
    return UserOut(id=current_user.id, email=current_user.email)
