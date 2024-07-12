# import json
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.models import table_registry

# import uuid
# id=str(uuid.uuid4())


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), server_onupdate=func.now())

    # def __init__(self, **dictionary):
    #     # def __init__(self, dictionary):
    #     # self.__dict__.update(dictionary)
    #     # for k, v in dictionary.items():
    #     #     self.k = v
    #     # for k, v in dictionary.items():
    #     #     setattr(self, k, v)
    #     for key in dictionary:
    #         setattr(self, key, dictionary[key])
    #
    # def as_dict(self):
    #     # return { col.name: col.isoformat() if isinstance(col, (datetime, date, time)) else getattr(self, col.name) for col in self.__table__.columns}
    #     return {col.name: getattr(self, col.name) for col in self.__table__.columns}
    #
    # def as_json(self):
    #     return json.dumps(self.as_dict(), default=str)

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
