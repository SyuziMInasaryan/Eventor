
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.database.session import get_async_session
from src.database.models.category import Category
from src.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    # Проверяем, нет ли уже категории с таким именем
    result = await session.execute(
        select(Category).where(Category.name == category_in.name)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )

    category = Category(
        name=category_in.name,
        description=category_in.description,
    )
    session.add(category)
    await session.commit()
    await session.refresh(category)

    return category


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






