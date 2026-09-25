import asyncio
import datetime
from enum import StrEnum

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class GroupNames(StrEnum):
    group_33 = "09c33"
    group_34 = "09c34"
    group_35 = "09c35"
    group_41 = "09c41"


class SubjectNames(StrEnum):
    first_subject = "ВНЕДРЕНИЕ ИС"
    second_project = "УПР. и АВТ. БД"
    third_project = "ОСНОВЫ СТАНД. и СЕРТ."


class WorkNames(StrEnum):
    first_work = "УП 1"
    second_work = "УП 2"
    third_work = "УП 3"


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


# async def initialize_works() -> None:
#     from database.models import Work
#     async with SessionLocal() as session:
#         for title in WorkNames:
#             stmt = select(exists().where(Work.title == title))
#             is_exists = await session.scalar(stmt)
#             if is_exists:
#                 continue
#             work = Work(title=title)
#             session.add(work)
#         await session.commit()


# TODO
async def initialize_tasks() -> None:
    from database.models import Work, Group, Task, Subject
    async with SessionLocal() as session:
        groups : list[Group] = list((await session.scalars(
            select(Group)
        )).all())

        subjects: list[Subject] = list((await session.scalars(
            select(Subject)
        )).all())

        deadline = datetime.datetime(2030, 6, 12)
        works : list[str] = ["work1", "work2", "work3", "work4", "work5", "work6", "work7"]

        for work_name in works:
            for subject in subjects:
                is_work_exists = (await session.execute(select(Work.id).where(Work.title == work_name, Work.subject_id == subject.id))).scalar()
                if is_work_exists:
                    continue
                work = Work(title = work_name, description = "trolala", subject_id = subject.id , file = None)
                session.add(work)
                await session.flush()
                for group in groups:
                    session.add(
                        Task(
                            work_id = work.id,
                            group_id = group.id,
                            ended_at = deadline
                        )
                    )
        await session.commit()




engine = create_async_engine("sqlite+aiosqlite:///file_exchanger.db")
SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await initialize_groups()
    await initialize_subjects()

    # await initialize_works()
    await initialize_tasks()


# if __name__ == "__main__":
#     asyncio.run(init_db())
