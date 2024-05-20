"""Class to represent ToDo items."""

from dataclasses import dataclass


@dataclass
class Task:
    """Class representing a single task on the todo list."""

    position: int
    text: str
    status: str = "To do"

    def pretty_string(self) -> str:
        return f"│ {self.position}  {self.text:50} {self.status:^11} │"
