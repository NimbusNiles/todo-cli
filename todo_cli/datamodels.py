"""Class to represent ToDo items."""

from dataclasses import dataclass


@dataclass
class Task:
    """Class representing a single task on the todo list."""

    position: int
    text: str
    status: str = "To do"
