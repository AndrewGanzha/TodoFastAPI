from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Todo, User
from core.schemas.todo import TodoCreate


async def create(data: TodoCreate, db: AsyncSession, current_user: User) -> Todo:
    todo = Todo(todo=data.todo, user=current_user, user_id=current_user.id)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo