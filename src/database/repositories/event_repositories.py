from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.event import Event

class EventRepository:
    async def create_event(
        self,
        db_session: AsyncSession,
        *,
        name: str,
        description: str | None,
        category_id: int,
        author_id: int,
        image_path: str | None,
    ) -> Event:
        stmt = (
            insert(Event)
            .values(
                name=name,
                description=description,
                category_id=category_id,
                author_id=author_id,
                image_path=image_path,
            )
            .returning(Event)
        )

        result = await db_session.execute(stmt)
        return result.scalar_one()
