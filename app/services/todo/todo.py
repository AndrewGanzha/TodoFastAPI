from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Todo, User
from core.schemas.todo import TodoCreate, TodoUpdate, TodoDelete
from repository.todo import create as todo_create
from repository.todo import update as todo_update
from repository.todo import delete as todo_delete


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

async def delete_todo(
        data: TodoDelete,
        db: AsyncSession,
        current_user: User
) -> None:
    await todo_delete(data, db, current_user)

    return None