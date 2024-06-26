"""Class to represent the database storing the ToDo tasks."""

import json
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session

from todo_cli.datamodels import Subtask, Task, Base
from todo_cli.utils import log
from todo_cli.utils.json_encoder import EnhancedJSONEncoder

logger = log.get_logger(__name__)


class DB:
    """Class to represent the database."""

    db_path = "data/todo.db"
    tasks: list[Task]

    def __init__(self, debug: int = 0) -> None:
        """Initialize the database."""
        if debug > 0:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        folder = self.db_path.split("/")[0]
        if not os.path.exists(folder):
            logger.info(f"Database folder {folder} not found, created.")
            os.mkdir(folder)

        echo = True if debug == 2 else False
        engine = create_engine(f"sqlite:///{self.db_path}", echo=echo)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks from the database."""
        with self.Session.begin() as session:
            session.expire_on_commit = False
            logger.debug(f"Get all tasks.")
            tasks = session.query(Task).all()
        logger.debug(f"Found {len(tasks)} tasks in database.")
        return tasks

    def add(self, text: str) -> None:
        """Add a task to the database."""
        tasks = self.get_all_tasks()
        task = Task(position=len(tasks) + 1, text=text)
        logger.debug(f"Add task {task} to the database.")
        with self.Session.begin() as session:
            session.add(task)

    def add_subtask(self, position: int, text: str):
        """Add subtask to a todo list item."""
        with self.Session.begin() as session:

            task = session.query(Task).where(Task.position == position).first()
            if task is None:
                logger.error(f"No task with position {position} found.")
                return

            subposition = len(task.subtasks) + 1

            logger.debug(f"Found task at position {position}: {task.text}.")
            logger.debug(f"Task has {len(task.subtasks)} subtasks.")

            subtask = Subtask(
                position=subposition, text=text, task=task, task_id=task.id
            )

            logger.debug(f"Add subtask to task {position} at subposition {subposition}")
            task.subtasks.append(subtask)

    def remove(self, positions: list[int]) -> None:
        """Remove a task from the database."""
        logger.debug(f"Remove task at positions {positions}.")
        with self.Session.begin() as session:
            tasks_to_delete = (
                session.query(Task).filter(Task.position.in_(positions)).all()
            )
            for task in tasks_to_delete:
                session.delete(task)
            self.reposition(session)

    def reposition(self, session: Session) -> None:
        """Reassign positions for all tasks."""
        logger.debug(f"Reposition tasks.")
        for ind, task in enumerate(session.query(Task).all()):
            task.position = ind + 1

    def set_status(self, positions: list[int], status: str) -> None:
        """Set status of a task."""
        logger.debug(f"Set status of tasks {positions} to {status}.")
        with self.Session.begin() as session:
            tasks_to_change = (
                session.query(Task).filter(Task.position.in_(positions)).all()
            )
            for task in tasks_to_change:
                task.status = status
