from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Todo, User
from core.schemas.todo import TodoCreate, TodoUpdate
from repository.todo import create as todo_create
from repository.todo import update as todo_update


async def create_todo(
    data: TodoCreate,
    db: AsyncSession,
    current_user: User,
) -> Todo:
    todo = await todo_create(data, db, current_user)

    return todo

async def update_todo(
        data: TodoUpdate,
        db: AsyncSession,
        current_user: User,
) -> Todo:
    todo = await todo_update(data, db, current_user)
    return todo