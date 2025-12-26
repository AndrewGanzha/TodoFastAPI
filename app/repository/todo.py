from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import Todo, db_helper, User
from core.schemas.todo import TodoCreate
from services.auth.deps import get_current_user


async def create(
    data: TodoCreate,
    db,
    current_user,
) -> Todo:
    todo = Todo(todo=data.todo, user=current_user, user_id=current_user.id)
    db.add(todo)
    return todo
