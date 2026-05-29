from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
from ..config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    try:
        import backend.app.models.user  # noqa: F401
        import backend.app.models.crop  # noqa: F401
        import backend.app.models.weather  # noqa: F401
        import backend.app.models.prediction  # noqa: F401
        import backend.app.models.recommendation  # noqa: F401
    except ModuleNotFoundError:
        import app.models.user  # noqa: F401
        import app.models.crop  # noqa: F401
        import app.models.weather  # noqa: F401
        import app.models.prediction  # noqa: F401
        import app.models.recommendation  # noqa: F401
    Base.metadata.create_all(bind=engine)
