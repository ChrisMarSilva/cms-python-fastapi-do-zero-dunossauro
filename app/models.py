from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    # __table_args__ = {'sqlite_autoincrement': True}
    # __mapper_args__ = {'eager_defaults': True}

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), server_onupdate=func.now())
    # CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

    def __repr__(self) -> str:  # pragma: no cover
        return (
            'User('
            f'id={self.id!r}, '
            f'username={self.username!r}, '
            f'password={self.password!r}, '
            f'email={self.email!r}, '
            f'created_at={self.created_at!r}'
            f'updated_at={self.updated_at!r}'
            f')'
        )
