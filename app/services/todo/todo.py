from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User, db_helper, Todo
from core.schemas.todo import TodoCreate, TodoGet
from repository.todo import create as todo_create
from services.auth.deps import get_current_user


def create_todo(
    data: TodoCreate,
    db: AsyncSession,
    current_user
) -> Todo:
    todo = todo_create(data, db, current_user)

    return todo