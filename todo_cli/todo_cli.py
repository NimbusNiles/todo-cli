"""CLI interface to show/add/delete tasks from a ToDo list."""

import argparse

from todo_cli.utils import log

logger = log.get_logger(__name__)


def print_hello() -> None:
    """Print hello world."""
    logger.info("Say hello.")
    print("Hello world!")


def main(argv: list[str] | None = None) -> None:
    """Main method parsing the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-hi", "--hello", help="Print hello world.", action="store_true"
    )

    args = parser.parse_args(argv)

    if args.hello:
        print_hello()


if __name__ == "__main__":
    main()
