from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


engine = create_async_engine(settings.ASYNC_DATABASE_URL)  # создали движок БД
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)  # передали наш движок в создатель сессий


class Base(DeclarativeBase):
    pass