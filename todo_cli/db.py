"""Class to represent the database storing the ToDo tasks."""

import json
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session

from todo_cli.datamodels import Task, Base
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

    def load_db(self) -> None:
        """Load the database."""
        self.tasks = []
        if not os.path.exists(self.db_path):
            logger.info(
                f"Database file {self.db_path} not found, empty database loaded."
            )
            return

        with open(self.db_path, "r") as db:
            logger.debug(f"Load database from {self.db_path}")
            json_tasks = json.load(db)
            for json_task in json_tasks:
                task = Task(**json_task)
                logger.debug(f"Found task {task}")
                self.tasks.append(task)
            logger.debug(f"Database loaded with {len(self.tasks)} Tasks.")

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
        for position in positions:
            self.tasks[position - 1].status = status
        self.save()

    def save(self) -> None:
        """Save the database to disk."""
        with open(self.db_path, "w") as db:
            logger.debug(f"Save {len(self.tasks)} tasks to {self.db_path}.")
            json.dump(self.tasks, db, indent=2, cls=EnhancedJSONEncoder)
