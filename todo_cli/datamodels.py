"""Class to represent ToDo items."""

from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Base(MappedAsDataclass, DeclarativeBase):
    """Base class for the database."""

    pass


class Task(Base):
    """Class representing a single task on the todo list."""

    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    position: Mapped[int]
    text: Mapped[str]
    subtasks: Mapped[list["Subtask"]] = relationship(
        back_populates="task", cascade="all, delete-orphan", init=False
    )
    status: Mapped[str] = mapped_column(default="To Do")

    def pretty_string(self) -> str:
        return f"│ {self.position}  {self.text:50} {self.status:^11} │"


class Subtask(Base):
    """Class representing a subtask of the main task of the todo list."""

    __tablename__ = "subtask"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    position: Mapped[int]
    text: Mapped[str]
    task: Mapped[Task] = relationship(back_populates="subtasks")
    task_id: Mapped[int] = mapped_column(ForeignKey(Task.id))
    status: Mapped[str] = mapped_column(default="To Do")
