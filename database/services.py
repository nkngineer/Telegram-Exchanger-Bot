from database.database import SessionLocal
from database.models import Work, Student, Group, Subject, Task
from pathlib import Path
from sqlalchemy import select, exists, Row


async def document_to_binary(file_path : Path) -> bytes:
    """
    Load a file into a memory as bytes.

    :param file_path: path to file
    :return: bytes of binary data
    """
    with open(file_path, "rb") as file:
        binary_data = file.read()

    return binary_data


async def check_group(group_name: str | None) -> bool:
    """
    Check if a group with the given name exists.

    :param group_name: user group name or None
    :return: True if the group exists, False otherwise
    """
    if group_name is None:
        return False
    async with SessionLocal() as session:
        return await session.scalar(
            select(exists().where(Group.name == group_name))
        )


async def check_user_profile(telegram_id: int) -> tuple[int,str] | None:
    """
    Look up and returns the user data(corporate id and group name)

    :param telegram_id: user telegram id
    :return: tuple of the student's corporate id and Group name, or None
    :note: open its own session via SessionLocal() .join() students
    """
    async with SessionLocal() as session:
        stmt = (
            select(Student.corporate_id, Group.name)
            .join(Group, Group.id == Student.group_id)
            .where(Student.telegram_id == telegram_id)
        )

        result = await session.execute(stmt)
        user_data : tuple[int,str] = result.tuples().fetchone()

        return user_data




async def get_subjects() -> list[Row[tuple[int, str]]]:
    async with SessionLocal() as session:
        stmt = select(Subject.id, Subject.name).order_by(Subject.name)
        return (await session.execute(stmt)).all()



async def get_groups() -> list[Row[tuple[int, str]]]:
    async with SessionLocal() as session:
        stmt = select(Group.id, Group.name).order_by(Group.name)
        return (await session.execute(stmt)).all()



# TODO
async def get_works(callback_lesson_id : str) -> list[Row[tuple[int, str]]]:
    # callback_lesson_id: subject_{subject.id}
    async with SessionLocal() as session:
        stmt = select(Work.id, Work.name).order_by(Work.name)
        return (await session.execute(stmt)).all()



async def check_lessons() -> tuple[str, ...]:
    async with SessionLocal() as session:
        stmt = select(Subject.name)
        result = await session.execute(stmt)
        return tuple(result.scalars().all())


async def check_user_authentication(telegram_id: int) -> bool:
    """
    Check if a user with the given telegram_id exists and has non-null group and corporate IDs.
    :param telegram_id:
    :return: True if the user exists, False otherwise
    """
    async with SessionLocal() as session:
        stmt = select(exists().where(Student.telegram_id == telegram_id, Student.group_id.is_not(None), Student.corporate_id.is_not(None))).limit(1)
        is_exists = await session.scalar(stmt)
        return is_exists


async def register_user(telegram_id : int, corporate_id : int, group_name: str) -> None:
    """
    Insert a new user with his telegram, corporate id and group name.
    :param telegram_id:
    :param corporate_id:
    :param group_name:
    :return: None
    :note: opens its own session via SessionLocal() with the students. Check ``groups.id`` by the ``groups.name``
    and then inserts a ``Student`` row with the resolved group_id
    """
    async with SessionLocal() as session:
        group_id = await session.scalar(select(Group.id).where(Group.name == group_name))
        stmt = select(Student).where(Student.telegram_id == telegram_id)
        student = await session.scalar(stmt)

        if student:
            student.corporate_id = corporate_id
            student.group_id = group_id
        else:
            student = Student(corporate_id = corporate_id, telegram_id = telegram_id, group_id = group_id)
            session.add(student)

        await session.commit()


async def set_user_group(callback_data: str | None, telegram_id: int) -> None:
    """
    Select group to the user
    :param callback_data:
    :param telegram_id:
    :raises ValueError: if the callback_data is None or if group/student is not found
    :return: None
    :note: opens its own session via SessionLocal(). Checks ``groups.name`` and resolves ``groups.id``, for the
    matching telegram_id
    """
    if callback_data is None:
        raise ValueError("callback_data cannot be None")
    async with SessionLocal() as session:
        group = await session.scalar(select(Group).where(Group.name == callback_data))
        user = await session.scalar(select(Student).where(Student.telegram_id == telegram_id))
        if group is None:
            raise ValueError(f"Группа {callback_data!r} не найдена")
        if user is None:
            raise ValueError(f"Студент с telegram_id = {telegram_id} не найден")
        user.group_id = group.id
        await session.commit()



async def insert_work(subject_id: int, file_path: Path) -> None:
    """
    Inserts new work as BLOB using document_to_binary()
    :param subject_id:
    :param file_path:
    :return: None
    :note: Calls document_to_binary(), which returns bytes of the file at ``file_path``
    """
    data = await document_to_binary(file_path)
    async with SessionLocal() as session:
        work = Work(subject_id = subject_id, file = data)
        session.add(work)
        await session.commit()

