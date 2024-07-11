from datetime import datetime, date, time
import json

import redis
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session, Mapped, mapped_column, registry


table_registry = registry()


def get_session():
    engine = create_engine("sqlite:///database.db", echo=False, connect_args={'check_same_thread': False})
    return Session(engine)


def get_cache():
    session = redis.ConnectionPool(host='localhost', port=6379, password='123', db=0, encoding="utf-8", decode_responses=True)
    return redis.Redis(connection_pool=session)


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), server_onupdate=func.now())

    # def __init__(self, dictionary):
    def __init__(self, **dictionary):
        # self.__dict__.update(dictionary)
        for key in dictionary:
            setattr(self, key, dictionary[key])
        # for k, v in dictionary.items():
        #     self.k = v
        # for k, v in dictionary.items():
        #     setattr(self, k, v)

    def as_dict(self):
        # return {col.name: col.isoformat() if isinstance(col, (datetime, date, time)) else getattr(self, col.name) for col in self.__table__.columns}
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def as_json(self):
        return json.dumps(self.as_dict(), default=str)


def main():
    try:
        session = get_session()
        stmt = select(User).where(User.id == 1)
        result = session.execute(stmt)
        db_user = result.scalar()
        print(f"session.user: {db_user}")
    except Exception as ex:
        print(f"session.user.error: {ex}")

    cache = get_cache()
    try:
        cache_chave =f"users_email_{db_user.email}"

        try:
            print(f"cache.set: {db_user.as_json()}")
            cache.set(cache_chave, db_user.as_json())
        except Exception as ex:
            print(f"cache.set.error: {ex}")

        try:
            cache_user = cache.get(cache_chave)
            print(f"cache.get: {type(cache_user)} --> {cache_user}")
        except Exception as ex:
            print(f"cache.get.error: {ex}")

        try:
            loads_user = json.loads(cache_user)
            # loads_user = json.loads(cache_user, object_hook=lambda x: User(**x))
            print(f"json.loads: {type(loads_user)} --> {loads_user}")
        except Exception as ex:
            print(f"json.loads.error: {ex}")
        try:
            new_user = User(**loads_user)
            print(f"new.user: {type(new_user)} --> {new_user}")
        except Exception as ex:
            print(f"new.user.error: {ex}")

        try:
            print(f"db_user.id: {db_user.id}")
            print(f"loads_user.id: {loads_user['id']}")
            print(f"new_user.id: {new_user.id}")
        except Exception as ex:
            print(f"user.id.error: {ex}")

    finally:
        cache.close()


if __name__ == "__main__":
    # asyncio.run(main())
    main()
