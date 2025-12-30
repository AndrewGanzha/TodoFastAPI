from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import Todo, User
from core.schemas.todo import TodoCreate, TodoUpdate, TodoDelete


async def create(data: TodoCreate, db: AsyncSession, current_user: User) -> Todo:
    todo = Todo(todo=data.todo, user=current_user, user_id=current_user.id)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo

async def update(data: TodoUpdate, db: AsyncSession, current_user: User) -> Todo:
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

async def get_all(
    db: AsyncSession,
    current_user: User,
    *,
    offset: int,
    limit: int,
) -> List[Todo]:
    stmt = (
        select(Todo)
        .where(Todo.user_id == current_user.id)
        .order_by(Todo.id)
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def delete(data: TodoDelete, db: AsyncSession, current_user: User) -> None:
    todo = await db.get(Todo, data.id)

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        await db.delete(todo)
        await db.commit()

    return None
