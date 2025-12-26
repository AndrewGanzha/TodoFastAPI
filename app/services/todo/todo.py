from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Todo, User
from core.schemas.todo import TodoCreate
from repository.todo import create as todo_create


async def create_todo(
    data: TodoCreate,
    db: AsyncSession,
    current_user: User,
) -> Todo:
    todo = await todo_create(data, db, current_user)

    return todo
