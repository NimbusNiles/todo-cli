"""CLI interface to show/add/delete tasks from a ToDo list."""

import argparse
import logging

from todo_cli.db import DB
from todo_cli.utils import log

logger = log.get_logger(__name__)


def print_hello(debug: int = 0) -> None:
    """Print hello world."""
    logger.debug(f"Say hello with debug level: {debug}.")
    print("Hello world!")


def add_task(text: str, debug: int) -> None:
    """Add new task to todo list."""
    db = DB(debug=debug)
    db.add(text=text)


def remove_task(positions: list[int], debug: int) -> None:
    """Remove a task from the todo list."""
    db = DB(debug=debug)
    db.remove(positions=positions)


def start_task(positions: list[int], debug: int) -> None:
    """Complete a task from the todo list."""
    db = DB(debug=debug)
    db.set_status(positions, status="In progress")


def stop_task(positions: list[int], debug: int) -> None:
    """Complete a task from the todo list."""
    db = DB(debug=debug)
    db.set_status(positions, status="To Do")


def complete_task(positions: list[int], debug: int) -> None:
    """Complete a task from the todo list."""
    db = DB(debug=debug)
    db.set_status(positions, status="Done!")


def add_subtask(position: int, text: str, debug: int) -> None:
    """Add subtask to a task in the todo list."""
    db = DB(debug=debug)
    db.add_subtask(position=position, text=text)


def show_list(debug: int) -> None:
    """Show list of todo items"""
    db = DB(debug=debug)
    print("╭" + "─" * 67 + "╮")
    tasks = db.get_all_tasks()
    if tasks == []:
        print(f"│{'(empty)':^67}│")
    for task in tasks:
        print(task.pretty_string())
    print("╰" + "─" * 67 + "╯")


def main(argv: list[str] | None = None) -> None:
    """Main method parsing the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-hi", "--hello", help="Print hello world.", action="store_true"
    )
    parser.add_argument("-d", help="Debug", action="count", default=0)
    parser.add_argument("-add", help="Add a new task.")
    parser.add_argument("-addsub", help="Add a new subtask.", nargs=2)
    parser.add_argument("-remove", help="Remove a task by id.", type=int, nargs="*")
    parser.add_argument("-start", help="Start task by id.", type=int, nargs="*")
    parser.add_argument("-stop", help="Stop task by id.", type=int, nargs="*")
    parser.add_argument("-complete", help="Complete task by id.", type=int, nargs="*")

    args = parser.parse_args(argv)

    if args.d:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if args.hello:
        print_hello(args.d)
        return

    if args.add:
        add_task(args.add, debug=args.d)

    if args.remove:
        remove_task(args.remove, debug=args.d)

    if args.start:
        start_task(args.start, debug=args.d)
    if args.stop:
        stop_task(args.stop, debug=args.d)
    if args.complete:
        complete_task(args.complete, debug=args.d)

    if args.addsub:
        task_position = args.addsub[0]
        subtask_text = args.addsub[1]
        add_subtask(task_position, subtask_text, debug=args.d)

    show_list(args.d)


if __name__ == "__main__":
    main()
