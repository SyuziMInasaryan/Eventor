from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ...database.repositories.category_repositories import CategoryRepository
from ...database.repositories.event_repositories import EventRepository
from ...database.repositories.user_repositories import UserRepository
from ...utils.files import save_event_image
from ...database.session import get_async_session
from ...schemas.event import EventRead

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/create", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(
    name: str = Form(...),
    description: str | None = Form(None),
    category_id: int = Form(...),
    author_id: int = Form(...),
    image: UploadFile | None = File(None),
    db_session: AsyncSession = Depends(get_async_session),
):
    # проверяем автора
    user_repo = UserRepository()
    author = await user_repo.get_user_by_id(session=db_session, user_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="User not found")

    # проверяем категорию
    category_repo = CategoryRepository()
    category = await category_repo.get_category_by_id(id=category_id, session=db_session)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    # сохраняем картинку
    image_path = None
    if image:
        image_path = await save_event_image(image)

    # создаем event
    event_repo = EventRepository()
    try:
        event = await event_repo.create_event(
            db_session=db_session,
            name=name,
            description=description,
            category_id=category_id,
            author_id=author_id,
            image_path=image_path,
        )
        await db_session.commit()
        await db_session.refresh(event)
        return event

    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(status_code=409, detail="Event already exists")

    except Exception:
        await db_session.rollback()
        raise
