from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import LargeBinary

from database.database import Base


class Work(Base):
    __tablename__ = "work"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"), nullable = True)
    file: Mapped[bytes] = mapped_column(LargeBinary, deferred = True, nullable = True)


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    starts_at: Mapped[datetime] = mapped_column(default=datetime.now())
    ended_at: Mapped[datetime] = mapped_column(nullable=True)  # TODO
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
    work_id: Mapped[int] = mapped_column(ForeignKey("work.id"))


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    corporate_id: Mapped[int]
    telegram_id: Mapped[int]
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), nullable=True)


class StudentTaskCompleted(Base):
    __tablename__ = "student_task_completed"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    file: Mapped[bytes] = mapped_column(LargeBinary, deferred=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

