"""Tests for the ToDo CLI."""

from todo import todo_cli


def test_hello(capsys) -> None:
    todo_cli.main(["-hi"])
    out, err = capsys.readouterr()
    assert out == "Hello world!\n"
