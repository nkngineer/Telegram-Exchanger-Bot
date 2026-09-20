from database.database import SessionLocal
from database.models import Work, Student, Group
from pathlib import Path
from sqlalchemy import select, exists




async def document_to_binary(file_path : Path) -> bytes:
    with open(file_path, "rb") as file:
        binary_data = file.read()

    return binary_data


async def check_group(group_name: str | None) -> bool:
    if group_name is None:
        return False
    async with SessionLocal() as session:
        return await session.scalar(
            select(exists().where(Group.name == group_name))
        ) or False


async def check_user_profile(telegram_id: int) -> tuple[str]:
    async with SessionLocal() as session:
        from sqlalchemy import select

        stmt = (
            select(Student.first_name, Student.last_name, Group.name)
            .join(Group, Group.id == Student.group_id)
            .where(Student.telegram_id == telegram_id)
        )

        result = await session.execute(stmt)

        user_data = result.tuples().fetchone()

        return user_data




async def check_user_name(username: str, telegram_id: int) -> None:
    async with SessionLocal() as session:
        all_name = username.split()
        first_name = all_name[0]
        last_name = all_name[1]
        stmt = select(exists().where(Student.first_name == first_name, Student.last_name == last_name))
        is_exists = await session.scalar(stmt)
        if not is_exists:
            await add_user(username, telegram_id)
        else:
            raise ValueError("Пользователь уже существует")



async def check_user_authorization(telegram_id: int) -> bool:
    async with SessionLocal() as session:
        stmt = select(exists().where(Student.telegram_id == telegram_id, Student.group_id != None))
        is_exists = await session.scalar(stmt)
        return is_exists


async def add_user(username: str, telegram_id: int) -> None:
    async with SessionLocal() as session:
        all_name = username.split()
        first_name = all_name[0]
        last_name = all_name[1]
        student = Student(first_name=first_name, last_name=last_name, telegram_id=telegram_id)
        session.add(student)
        await session.commit()



async def group_menu() -> None:
    async with SessionLocal() as session:
        groups = (await session.scalars(select(Group.name))).all()
        print(groups)



async def set_user_group(callback_data: str|None, telegram_id: int) -> None:
    async with SessionLocal() as session:
        group = await session.scalar(select(Group).where(Group.name == callback_data))
        user = await session.scalar(select(Student).where(Student.telegram_id == telegram_id))
        user.group_id = group.id
        await session.commit()



async def add_work(subject_id: int, file_path: Path) -> None:
    data = await document_to_binary(file_path)
    async with SessionLocal() as session:
        work = Work(subject_id=subject_id, file=data)
        session.add(work)
        await session.commit()

