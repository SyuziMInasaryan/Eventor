from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.repositories.user_repositories import UserRepository
from src.database.session import get_async_session
from src.schemas.user import UserCreate, UserOut
from src.service.user_services import UserService, EmailAlreadyExists, UsernameAlreadyExists

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service() -> UserService:
    # можно заменить на нормальный DI-контейнер позже, но так уже чисто и понятно
    return UserService(UserRepository())


@router.post("/create", response_model=UserOut, status_code=201)
async def create_user(
        data: UserCreate,
        session: AsyncSession = Depends(get_async_session),
        service: UserService = Depends(get_user_service),
):
    try:
        return await service.create_user(session, data)

    except EmailAlreadyExists:
        raise HTTPException(status_code=409, detail="Email already in use")

    except UsernameAlreadyExists:
        raise HTTPException(status_code=409, detail="Username already in use")

    except IntegrityError:
        # если случилась гонка, говорим тем же 409
        raise HTTPException(status_code=409, detail="Email or username already exists")
