"""Test the database"""

import os
from todo_cli.datamodels import Task
from todo_cli.db import DB


def test_db_init() -> None:
    """Test database initialization."""
    db = DB(debug=1)
    assert isinstance(db, DB)
    assert isinstance(db.db_path, str)


def test_db_add() -> None:
    """Test adding a task to the database."""
    db = DB(debug=1)
    db.add("Test")
    assert len(db.tasks) > 0
    assert isinstance(db.tasks[0], Task)
