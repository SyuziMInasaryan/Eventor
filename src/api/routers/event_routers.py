
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src import schemas
from src.database.models import Category, User
from src.database.session import get_async_session
from src.database.models.event import Event
from src.schemas.category import CategoryRead, CategoryUpdate
from src.schemas.event import EventCreate, EventUpdate, EventRead

router = APIRouter(
    prefix="/events",
    tags=["events"],
)

@router.post(
    "/create",
    response_model=EventRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    name: str = Form(...),
    description: str | None = Form(None),
    category_id: int = Form(...),
    author_id: int = Form(...),
    image: UploadFile = File(None),
    db_session: AsyncSession = Depends(get_async_session),
):
    # проверка дубликата по имени
    result = await db_session.execute(
        select(Event).where(Event.name == name)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event with this name already exists",
        )

    # проверяем, что такая категория существует
    category = await db_session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")

    # проверяем, что такой автор существует
    author = await db_session.get(User, author_id)
    if not author:
        raise HTTPException(status_code=400, detail="Author not found")

    # читаем картинку
    image_data = await image.read() if image else None

    event = Event(
        name=name,
        description=description,
        image=image_data,
        category_id=category_id,
        author_id=author_id,
    )

    db_session.add(event)
    await db_session.commit()
    await db_session.refresh(event)

    return event


@router.get(
    "/",
    response_model=List[CategoryRead],
)
async def list_categories(
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    return categories

@router.get("/{id}", response_model=CategoryRead)
async def get_category(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.get(Category, id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return result

@router.delete('/delete/{id}')
async def delete_category(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    category = await session.get(Category, id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(category)
    await session.commit()

    return {"message": "Successfully deleted"}

@router.put('/cat_update/{id}')
async def update_category(
    id: int,
    category_update: CategoryUpdate,
    session: AsyncSession = Depends(get_async_session),):
    result = await session.execute(select(Category).where(Category.id == id))
    category = result.scalar()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    stmt = (
            update(Category)
            .where(Category.id == id)
            .values(**category_update.model_dump())
            .returning(Category)
        )

    result = await session.scalar(stmt)
    await session.commit()

    return result