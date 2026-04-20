from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(
    settings.database_url,
    pool_recycle=3600,
    echo=settings.debug
    )

SessionLocal = sessionmaker(
    bind=engine,
    autocommit = False,
    autoflush=False
    )

class Base(DeclarativeBase):
    pass
