"""CLI interface to show/add/delete tasks from a ToDo list."""

import argparse


def print_hello() -> None:
    """Print hello world."""
    print("Hello world!")


def main() -> None:
    """Main method parsing the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-hi", "--hello", help="Print hello world.", action="store_true"
    )

    args = parser.parse_args()

    if args.hello:
        print_hello()


if __name__ == "__main__":
    main()
