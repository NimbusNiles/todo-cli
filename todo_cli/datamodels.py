"""Class to represent ToDo items."""

from dataclasses import dataclass


@dataclass
class Task:
    """Class representing a single task on the todo list."""

    position: int
    text: str
    status: str = "To do"

    def __str__(self) -> str:
        return f"│ {self.position}   " f"{self.text:50}   " f"{self.status:^11} │"
