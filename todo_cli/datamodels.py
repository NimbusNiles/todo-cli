"""Class to represent ToDo items."""

from dataclasses import dataclass
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import Mapped, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    """Base class for the database."""

    pass


class Task(Base):
    """Class representing a single task on the todo list."""

    __tablename__ = "task"

    position: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    status: Mapped[str] = mapped_column(default="To Do")

    def pretty_string(self) -> str:
        return f"│ {self.position}  {self.text:50} {self.status:^11} │"
