"""SQLite 异步引擎 & 会话工厂"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.utils.config import SQLITE_PATH

engine = create_async_engine(SQLITE_PATH, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    """FastAPI 依赖：每次请求提供一个异步 Session"""
    async with async_session() as session:
        yield session


async def init_db():
    """启动时调用，自动建表"""
    from app.models import Base  # noqa: PLC0415 避免循环导入

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
