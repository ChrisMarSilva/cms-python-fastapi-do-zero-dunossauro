# from typing import AsyncGenerator

# from fastapi import HTTPException
# from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.utils.settings import Settings

settings = Settings()
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO, connect_args={'check_same_thread': False})


async def get_session() -> AsyncSession:  # pragma: no cover
    async with AsyncSession(engine) as session:
        # try:
        yield session
        #     await session.commit()
        # except SQLAlchemyError as sql_ex:
        #     await session.rollback()
        #     raise sql_ex
        # except HTTPException as http_ex:
        #     await session.rollback()
        #     raise http_ex
        # finally:
        #     await session.close()
