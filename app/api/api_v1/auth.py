from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from repository.users import get_user_by_email, create_user
from schemas.user import UserOut, UserRegisterIn, TokenOut, LoginIn
from services.auth.deps import get_current_user
from services.auth.jwt import create_access_token
from services.auth.security import hash_password, verify_password

# TODO заменить на использование env
SECRET_KEY = "CHANGE_ME"

router = APIRouter()

@router.post("/auth/register", response_model=UserOut, status_code=201)
async def register(data: UserRegisterIn, db: AsyncSession = Depends(db_helper.session_getter)):
    existing = await get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await create_user(db, email=data.email, username=data.username, password_hash=hash_password(data.password))
    return UserOut(id=user.id, email=user.email)

@router.post("/auth/login", response_model=TokenOut)
async def login(data: LoginIn, db: AsyncSession = Depends(db_helper.session_getter)):
    user = await get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id), secret_key=SECRET_KEY, expires_minutes=30)
    return TokenOut(access_token=token)

@router.get("/me", response_model=UserOut)
async def me(current_user=Depends(get_current_user(SECRET_KEY))):
    return UserOut(id=current_user.id, email=current_user.email)
