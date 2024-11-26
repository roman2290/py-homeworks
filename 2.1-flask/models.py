import os
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from sqlalchemy import String, func, DateTime, create_engine
import datetime
from sqlalchemy.ext.declarative import declarative_base


from config import (
POSTGRES_PASSWORD,
POSTGRES_USER,
POSTGRES_DB,
POSTGRES_HOST,
POSTGRES_PORT,
)

#PG_DSN = 'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5431/{POSTGRES_DB}'

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
#PG_DSN = 'postgresql://use:2204@localhost:5431/apps'
engine = create_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)



class Advertisement(Base):
    __tablename__ = "apps"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    time_of_creation: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String(100), index=True, nullable=False)

Base.metadata.create_all(engine)