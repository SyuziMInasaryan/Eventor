
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.database.repositories.category_repositories import CategoryRepository
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

    category_crud = CategoryRepository()
    existing = await category_crud.get_category_by_name(
        category_name=category_in.name,
        session=session
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )

    category = await category_crud.create_category(session=session,
                                                   category_in=category_in)
    await session.commit()
    return category

@router.get(
    "/",
    response_model=List[CategoryRead],
)
async def list_categories(
    session: AsyncSession = Depends(get_async_session),
):
    category_crud = CategoryRepository()
    categories = await category_crud.list_categories(session)
    return categories

@router.get("/{id}", response_model=CategoryRead)
async def get_category(
    id: int,
    session: AsyncSession = Depends(get_async_session)
):
    category_crud = CategoryRepository()
    result = await category_crud.get_category_by_id(id=id, session=session)

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
    category_crud = CategoryRepository()
    category = await category_crud.delete_category(id=id, session=session)

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    await session.commit()
    return category



@router.put('/cat_update/{id}')
async def update_category(
    id: int,
    category_update: CategoryUpdate,
    session: AsyncSession = Depends(get_async_session),):

    category_crud = CategoryRepository()
    category = await category_crud.update_category(id=id, category_update=category_update, session=session)

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    await session.commit()
    return category








