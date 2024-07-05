from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
from app.utils.settings import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO, connect_args={'check_same_thread': False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
# models.Base.metadata.create_all(bind=engine)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
