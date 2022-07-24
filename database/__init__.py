from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from config import SQLAlchemyConfig

engine = create_async_engine(**SQLAlchemyConfig())
BaseTable = declarative_base()

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
session = async_session()


async def init_tables():
    global session
    from . import tables

    async with engine.begin() as conn:
        # await conn.run_sync(BaseTable.metadata.drop_all)
        await conn.run_sync(BaseTable.metadata.create_all)
