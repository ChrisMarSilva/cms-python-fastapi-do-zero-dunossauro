from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.utils.settings import Settings
# from app.utils.tracing import instrument_async

settings = Settings()
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO, connect_args={'check_same_thread': False})
SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)  # , enable_commenter=True, commenter_options={}


# @instrument_async('calling get_session')
async def get_session() -> AsyncSession:  # pragma: no cover
    async with AsyncSession(engine) as session:
        yield session
