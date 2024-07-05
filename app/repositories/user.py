from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 100) -> [User]:
        stmt = select(User).offset(skip).limit(limit)
        return session.scalars(stmt).all()

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return session.scalar(stmt)

    @staticmethod
    def get_by_username(session: Session, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return session.scalar(stmt)

    @staticmethod
    def get_by_email(session: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return session.scalar(stmt)

    @staticmethod
    def get_by_username_or_email(session: Session, username: str, email: str) -> User | None:
        stmt = select(User).where((User.username == username) | (User.email == email))
        return session.scalar(stmt)

    @staticmethod
    def exists_by_id(session: Session, user_id: int) -> bool:
        stmt = select(User).where(User.id == user_id)
        return session.scalar(stmt) is not None

    @staticmethod
    def create(session: Session, user: User) -> User | None:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def update(session: Session, user: User) -> User | None:
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def delete(session: Session, user: User) -> None:
        session.delete(user)
        session.commit()
