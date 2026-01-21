from typing import List, Optional

from fastapi import  HTTPException, status
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import session
from src.database.models.category import Category
from src.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:   # Проверяем, нет ли уже категории с таким именем
    async def list_categories(
            self,
            session: AsyncSession
    ) -> List[Category]:
        result = await (session.execute
                        (select(Category)))
        categories = result.scalars().all()
        return categories

    async def get_category_by_name(
                self,
                category_name: str,
                session: AsyncSession
        ) -> Optional[Category]:

        result = await session.execute(
            select(Category).where(Category.name == category_name)
        )
        return result.scalar_one_or_none()

    async def create_category(self,
                category_in: CategoryCreate,
                session: AsyncSession):
        stmt = (
            insert(Category)
            .values(
                name=category_in.name,
                description=category_in.description,
            )
            .returning(Category)
        )

        category = (await session.execute(stmt)).scalar_one()

        return category

    async def get_category_by_id(self,
                                 id: int,
                                 session: AsyncSession) -> Optional[Category]:
        result = await session.execute(
            select(Category).where(Category.id == id))

        return result.scalar_one_or_none()

    async def delete_category(self,
                              id: int,
                              session: AsyncSession) :
        category = await session.get(Category, id)
        await session.delete(category)
        return {"message": "Successfully deleted"}

    async def update_category(self,
                              id: int,
                              category_update: CategoryUpdate,
                              session: AsyncSession
                              ):
        result = await session.execute(select(Category).where(Category.id == id))
        category = result.scalar()
        stmt = (
             update(Category)
            .where(Category.id == id)
            .values(**category_update.model_dump())
            .returning(Category)
        )

        result = await session.scalar(stmt)
        return result














