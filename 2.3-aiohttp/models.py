#! C:\Users\User\Desktop\py-homeworks\2.3-aiohttp\venv\Scripts\python.exe
import os
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, String, func, DateTime, Integer
import datetime
from typing import List
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)

from config import (
POSTGRES_PASSWORD,
POSTGRES_USER,
POSTGRES_DB,
POSTGRES_HOST,
POSTGRES_PORT,
)

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "aioapi")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_async_engine(PG_DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):

    __tablename__ = "user_apps"

    id:  Mapped[int] = mapped_column(Integer,  primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100))
    password:Mapped[str] = mapped_column(String, nullable=False)
    apps_advert: Mapped[List['Advertisement']] = relationship(back_populates = 'owner')

    @property
    def dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

class Advertisement(Base):

    __tablename__ = "apps_advert"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    time_of_creation: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner_id: Mapped[int] = mapped_column(ForeignKey('user_apps.id'))
    owner: Mapped[User] = relationship(User, back_populates = 'apps_advert')

    @property
    async def dict(self):
        owner = await self.awaitable_attrs.owner
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'time_of_creation': int(self.time_of_creation.timestamp()),
            'owner': owner.name
        }

async def init_db():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()