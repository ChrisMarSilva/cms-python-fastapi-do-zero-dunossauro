from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.tracing import instrument_async


class UserRepository:
    @staticmethod
    @instrument_async('calling UserRepository.get_all')
    async def get_all(session: AsyncSession, skip: int = 0, limit: int = 100) -> [User]:
        stmt = select(User).order_by(User.username, User.id).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    @instrument_async('calling UserRepository.get_by_id')
    async def get_by_id(session: AsyncSession, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    @instrument_async('calling UserRepository.get_by_username')
    async def get_by_username(session: AsyncSession, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    @instrument_async('calling UserRepository.get_by_email')
    async def get_by_email(session: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    @instrument_async('calling UserRepository.get_by_username_or_email')
    async def get_by_username_or_email(session: AsyncSession, username: str, email: str) -> User | None:
        stmt = select(User).where((User.username == username) | (User.email == email))
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    @instrument_async('calling UserRepository.exists_by_id')
    async def exists_by_id(session: AsyncSession, user_id: int) -> bool:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar() is not None

    @staticmethod
    @instrument_async('calling UserRepository.create')
    async def create(session: AsyncSession, user: User) -> User | None:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    @instrument_async('calling UserRepository.update')
    async def update(session: AsyncSession, user: User) -> User | None:
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    @instrument_async('calling UserRepository.delete')
    async def delete(session: AsyncSession, user: User) -> None:
        await session.delete(user)
        await session.commit()
