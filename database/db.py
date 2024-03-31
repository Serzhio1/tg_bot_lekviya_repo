from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=5, # maximum number of dataf[f[f[base connections
    max_overflow=10 # number of additional database connections
)

session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):

    metadata = MetaData()