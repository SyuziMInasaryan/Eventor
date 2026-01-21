from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from src.database.models import User
from src.database.repositories.user_repositories import UserRepository
from src.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class EmailAlreadyExists(Exception):
    pass

class UsernameAlreadyExists(Exception):
    pass

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, session, data: UserCreate) -> User:
        user = await self.repo.get_by_email(session, data.email)
        print("EMAIL CHECK RESULT:", user)  # ← ВОТ СЮДА

        if user:
            raise EmailAlreadyExists()

        user_by_username = await self.repo.get_by_username(session, data.username)
        print("USERNAME CHECK RESULT:", user_by_username)

        if user_by_username:
            raise UsernameAlreadyExists()

        user = User(
            email=data.email,
            username=data.username,
            password_hash=hash_password(data.password),
            is_active=True,
            is_admin=False,
        )

        await self.repo.create(session, user)

        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            print("INTEGRITY ERROR:", repr(e))
            # для asyncpg обычно самое полезное тут:
            print("ORIG:", repr(getattr(e, "orig", None)))
            raise

        await session.refresh(user)
        return user
