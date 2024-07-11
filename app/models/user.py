from datetime import datetime, date, time
import json

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
# from sqlalchemy_serializer import SerializerMixin

from app.models import table_registry


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    # serialize_only = ('id', 'email_id', 'role_type', 'users.id')
    # serialize_rules = ('-merchants')

    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), server_onupdate=func.now())

    def as_dict(self):
        try:
            # return self.__dict__
            # return self.to_dict()
            # return dict([(col, str(getattr(self, col))) for col in self.__table__.columns.keys()])
            return {
                col.name: col.isoformat() if isinstance(col, (datetime, date, time)) else getattr(self, col.name)
                for col in self.__table__.columns
            }
        except Exception as ex:
            print(f"Error as_dict: {ex}")
            return self.__dict__

    def as_json(self):
        try:
            # json.dumps(c.__dict__)
            # json.dumps(self, default=lambda x: x.__dict__)
            # json.dumps(dict(self), default=alchemy_encoder)
            return json.dumps(self.as_dict(), default=str)
        except Exception as ex:
            print(f"Error as_json: {ex}")

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
