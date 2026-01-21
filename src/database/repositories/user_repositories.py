import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User


class UserRepository:
    async def get_by_email(self, session: AsyncSession, email: str):
        stmt = sa.select(User).where(User.email == email)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_username(self, session: AsyncSession, username: str):
        stmt = sa.select(User).where(User.username == username)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_user_by_id(self, session: AsyncSession, user_id: int):
        stmt = sa.select(User).where(User.id == user_id)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    async def create(self, session: AsyncSession, user: User) -> User:
        session.add(user)
        return user