from typing import AsyncGenerator
from backend.app.core.config import settings
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from backend.app.core.logging import get_logger

logger = get_logger()

engine = create_async_engine(settings.DATABASE_URL)
# this basically means that session will not expire on commit, this is because
# we are using asyncio and we want to keep the session alive for the duration of the request
async_session = async_sessionmaker(
# async_sessionmaker is just a factory for creating satabase sessions
    engine,
    # the session will not automatically expire on commit, this is because we want to cover session lifecycle ourselves
    expire_on_commit=False,
    # the session is to be an instance of the asyncsession
    class_=AsyncSession,
)

# This dependency is going to be used to get the database session, which is going to be
# used as a dependency for our fast api application
async def det_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"An error occurred while getting the database session:"
                         f"{e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    pass