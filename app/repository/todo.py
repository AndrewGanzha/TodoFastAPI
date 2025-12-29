from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import Todo, User
from core.schemas.todo import TodoCreate, TodoUpdate


async def create(data: TodoCreate, db: AsyncSession, current_user: User) -> Todo:
    todo = Todo(todo=data.todo, user=current_user, user_id=current_user.id)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo

# TODO поправить типизацию
async def update(data: TodoUpdate, db: AsyncSession, current_user: User) -> Todo | None:
    todo = await db.get(Todo, data.id)

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        todo.todo = data.todo
        await db.commit()
        await db.refresh(todo)
        return todo
