import asyncio

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select, exists

from enum import StrEnum


class GroupNames(StrEnum):
    group_33 = "09c33"
    group_34 = "09c34"
    group_35 = "09c35"
    group_41 = "09c41"


class SubjectNames(StrEnum):
    first_subject = "ВНЕДРЕНИЕ ИС"
    second_project = "УПР. и АВТ. БД"
    third_project = "ОСНОВЫ СТАНД. и СЕРТ."


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


async def initialize_subjects() -> None:
    from database.models import Subject
    async with SessionLocal() as session:
        for name in SubjectNames:
            stmt = select(exists().where(Subject.name == name))
            is_exists = await session.scalar(stmt)
            if is_exists:
                continue
            subject = Subject(name=name)
            session.add(subject)
        await session.commit()



engine = create_async_engine("sqlite+aiosqlite:///file_exchanger.db")
SessionLocal = async_sessionmaker(bind = engine,class_ = AsyncSession, expire_on_commit = False, autoflush = False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await initialize_groups()
    await initialize_subjects()

# if __name__ == "__main__":
#     asyncio.run(init_db())