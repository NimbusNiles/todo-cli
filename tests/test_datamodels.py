"""Tests for datamodels"""

import pytest

from todo_cli.datamodels import Task


@pytest.fixture
def task() -> Task:
    return Task(position=1, text="Test")


def test_task_init(task: Task) -> None:
    """Test initialization of task"""
    assert isinstance(task, Task)
    assert task.position == 1
    assert task.text == "Test"
    assert task.status == "To Do"
