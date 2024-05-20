"""Methods to configure logging."""

import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

FILE = "logs/todo_cli.log"
FORMAT = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")


def get_console_handler() -> logging.StreamHandler:
    """Return a console handler to stdout."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(FORMAT)
    return handler


def get_file_handler() -> logging.FileHandler:
    """Return a file handler to logging file."""
    create_logging_folder_if_needed()
    handler = TimedRotatingFileHandler(FILE, when="midnight", backupCount=5, delay=True)
    handler.setFormatter(FORMAT)
    return handler


def create_logging_folder_if_needed() -> None:
    """Create the logging folder if it does not exist yet."""
    folder = FILE.split("/")[0]
    if not os.path.exists(folder):
        os.mkdir(folder)


def get_logger(name: str) -> logging.Logger:
    """Return a formatted logger with both a console and file handler."""
    logger = logging.getLogger(name)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.setLevel(logging.DEBUG)
    return logger
