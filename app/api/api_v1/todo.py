from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User, db_helper, Todo
from core.schemas.todo import TodoCreate, TodoGet, TodoUpdate, TodoDelete
from services.auth.deps import get_current_user
from services.todo.todo import create_todo as create_todo_service, delete_todo
from services.todo.todo import update_todo as update_todo_service

router = APIRouter()


@router.post("/create", response_model=TodoGet)
async def create_todo_endpoint(
    data: TodoCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user(settings.auth.access_secret_key)),
) -> Todo:
    return await create_todo_service(data, db, current_user)

@router.post("/update", response_model=TodoGet)
async def update_todo_endpoint(
    data: TodoUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(get_current_user(settings.auth.access_secret_key)),
)-> Todo:
    return await update_todo_service(data, db, current_user)

@router.post("/delete", response_model=None)
async def delete_todo_endpoint(
        data: TodoDelete,
        db: AsyncSession = Depends(db_helper.session_getter),
        current_user: User = Depends(get_current_user(settings.auth.access_secret_key)),
) -> None:
    return await delete_todo(data, db, current_user)