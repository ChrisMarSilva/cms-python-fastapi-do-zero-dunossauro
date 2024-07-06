from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    @staticmethod
    async def get_all(session: AsyncSession, skip: int = 0, limit: int = 100) -> [User]:
        stmt = select(User).offset(skip).limit(limit)
        result = await session.scalars(stmt)
        return result.all()

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await session.scalar(stmt)
        return result

    @staticmethod
    async def get_by_username(session: AsyncSession, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await session.scalar(stmt)
        return result

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_by_username_or_email(session: AsyncSession, username: str, email: str) -> User | None:
        stmt = select(User).where((User.username == username) | (User.email == email))
        result = await session.scalar(stmt)
        return result

    @staticmethod
    async def exists_by_id(session: AsyncSession, user_id: int) -> bool:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar() is not None

    @staticmethod
    async def create(session: AsyncSession, user: User) -> User | None:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def update(session: AsyncSession, user: User) -> User | None:
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def delete(session: AsyncSession, user: User) -> None:
        await session.delete(user)
        await session.commit()
