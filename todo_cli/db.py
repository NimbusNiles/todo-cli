"""Class to represent the database storing the ToDo tasks."""

import json
import os

from todo_cli.datamodels import Task
from todo_cli.utils import log
from todo_cli.utils.json_encoder import EnhancedJSONEncoder

logger = log.get_logger(__name__)


class DB:
    """Class to represent the database."""

    db_path = "data/db.json"
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

        self.load_db()

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
            for task in json_tasks:
                self.tasks.append(Task(*task))
            logger.debug(f"Database loaded with {len(self.tasks)} Tasks.")

    def add(self, text: str) -> None:
        """Add a task to the database."""
        task = Task(position=len(self.tasks) + 1, text=text)
        logger.debug(f"Add task {task} to the database.")
        self.tasks.append(task)
        self.save()

    def save(self) -> None:
        """Save the database to disk."""
        with open(self.db_path, "w") as db:
            logger.debug(f"Save {len(self.tasks)} tasks to {self.db_path}.")
            json.dump(self.tasks, db, indent=2, cls=EnhancedJSONEncoder)