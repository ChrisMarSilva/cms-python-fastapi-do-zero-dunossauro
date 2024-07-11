from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from opentelemetry import trace

from app.utils.settings import Settings
# from app.utils.tracing import instrument_async

settings = Settings()
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO, connect_args={'check_same_thread': False})
SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)  # , enable_commenter=True, commenter_options={}
tracer = trace.get_tracer(__name__)


# @instrument_async('calling get_session')
async def get_session() -> AsyncSession:  # pragma: no cover
    with tracer.start_as_current_span('get_session'):
        async with AsyncSession(engine) as session:
            yield session
