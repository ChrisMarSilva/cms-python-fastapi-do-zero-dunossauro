from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.utils.settings import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
    # db = SessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()
