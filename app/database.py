from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.settings import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
