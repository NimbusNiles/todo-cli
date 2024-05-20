"""CLI interface to show/add/delete tasks from a ToDo list."""

import argparse
import logging

from todo_cli.db import DB
from todo_cli.utils import log

logger = log.get_logger(__name__)


def print_hello() -> None:
    """Print hello world."""
    logger.debug("Say hello.")
    print("Hello world!")


def add_task(text: str, debug: bool) -> None:
    """Add new task to todo list."""
    db = DB(debug=int(debug))
    db.add(text=text)


def remove_task(positions: list[int], debug: bool) -> None:
    """Remove a task from the todo list."""
    db = DB(debug=int(debug))
    db.remove(positions=positions)


def show_list(debug: bool) -> None:
    """Show list of todo items"""
    db = DB(debug=int(debug))
    print("╭" + "─" * 67 + "╮")
    for task in db.tasks:
        print(task.pretty_string())
    print("╰" + "─" * 67 + "╯")


def main(argv: list[str] | None = None) -> None:
    """Main method parsing the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-hi", "--hello", help="Print hello world.", action="store_true"
    )
    parser.add_argument("-d", help="Debug", action="store_true")
    parser.add_argument("-add", help="Add a new task.")
    parser.add_argument("-remove", help="Remove a task by id.", type=int, nargs="*")

    args = parser.parse_args(argv)

    if args.d:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if args.hello:
        print_hello()
        return

    if args.add:
        add_task(args.add, debug=args.d)

    if args.remove:
        remove_task(args.remove, debug=args.d)

    show_list(args.d)


if __name__ == "__main__":
    main()
