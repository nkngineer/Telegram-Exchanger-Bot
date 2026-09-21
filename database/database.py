import asyncio

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select, exists

from enum import StrEnum


class GroupNames(StrEnum):
    group_33 = "09c33"
    group_34 = "09c34",
    group_35 = "09c35",
    group_41 = "09c41",


class SubjectNames(StrEnum):
    pass


class Base(DeclarativeBase):
    pass



async def initialize_groups() -> None:
    """
    Initialize groups in the database with missing rows from GroupNames
    :return: None
    """
    from database.models import Group
    async with SessionLocal() as session:
        for name in GroupNames:
            stmt = select(exists().where(Group.name == name))
            is_exists = await session.scalar(stmt)
            if is_exists:
                continue
            group = Group(name=name)
            session.add(group)
        await session.commit()


# TODO
async def initialize_subjects() -> None:
    """
    Initialize subjects in the database with missing rows from SubjectNames
    :return: None
    """
    pass


engine = create_async_engine("sqlite+aiosqlite:///file_exchanger.db")
SessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession, expire_on_commit=False, autoflush=False)




async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await initialize_groups()

# if __name__ == "__main__":
#     asyncio.run(init_db())