#! C:\Users\User\Desktop\py-homeworks\2.2-asyncio\venv\Scripts\python.exe



import os
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import JSON, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs, async_sessionmaker

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "swapi")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass

class Person(Base):
    __tablename__ = "character"


    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(100))
    eye_color: Mapped[str] = mapped_column(String(50))
    films: Mapped[Text] = mapped_column(Text)
    gender: Mapped[str] = mapped_column(String(100))
    hair_color: Mapped[str] = mapped_column(String(100))
    height: Mapped[str] = mapped_column(String(1000), nullable=False)
    homeworld: Mapped[str] = mapped_column(String(100))
    mass: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(50), nullable= False)
    skin_color: Mapped[str] = mapped_column(String(100))
    species: Mapped[Text] = mapped_column(Text)
    starships: Mapped[Text] = mapped_column(Text)
    vehicles: Mapped[Text] = mapped_column(Text)

 
async def init_orm():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()