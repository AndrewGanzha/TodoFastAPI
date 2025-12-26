from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User
from core.schemas.todo import TodoGet, TodoCreate
from services.auth.deps import get_current_user
from services.todo.todo import create_todo

router = APIRouter()

@router.post("/todo", response_model=TodoGet)
def create_todo_endpoint(data: TodoCreate,     db: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user(settings.auth.access_secret_key)),):
    return create_todo(data, db, current_user)