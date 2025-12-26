from core.models import Todo
from core.schemas.todo import TodoCreate


async def create(
    data: TodoCreate,
    db,
    current_user,
) -> Todo:
    todo = Todo(todo=data.todo, user=current_user, user_id=current_user.id)
    db.add(todo)
    return todo
