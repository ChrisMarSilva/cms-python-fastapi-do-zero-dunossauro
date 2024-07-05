from datetime import datetime

# from uuid import UUID, uuid4
# from enum import Enum
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

# from sqlalchemy import func, Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
from app.models import table_registry

# from app.database import Base

# class Gender(str, Enum):
#     male = 'male'
#     female = 'female'
#
#
# class Role(str, Enum):
#     admin = 'admin'
#     user = 'user'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), server_onupdate=func.now())
    # id: int = Column(Integer, primary_key=True, index=True)
    # titulo: str = Column(String(100), nullable=False)
    # descricao: str = Column(String(255), nullable=False)
    # carga_horaria: int = Column(Integer, nullable=False)
    # qtd_exercicios: int = Column(Integer, nullable=False)
    # id: Optional[UUID] = uuid4()
    # gender: Gender
    # roles: Optional[List[Role]]

    def __repr__(self) -> str:
        return (
            'User('
            f'id={self.id!r}, '
            f'username={self.username!r}, '
            f'password={self.password!r}, '
            f'email={self.email!r}, '
            f'created_at={self.created_at.strftime("%d-%m-%Y %H:%M:%S")!r}, '
            f'updated_at={self.updated_at.strftime("%d-%m-%Y %H:%M:%S")!r}'
            f')'
        )


# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#
#     items = relationship("Item", back_populates="owner")
#
#
# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#
#     owner = relationship("User", back_populates="items")
