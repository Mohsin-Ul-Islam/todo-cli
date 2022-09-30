#!/usr/bin/env python

import sys
import json
import pathlib
import argparse

HOME = str(pathlib.Path.home())
FILE_PATH = f"{HOME}/.todo/todos.json"


def create_todo_files() -> None:

    pathlib.Path(f"{HOME}/.todo").mkdir(exist_ok=True)
    with open(FILE_PATH, "w+") as file_:
        json.dump([], file_)


def load() -> dict:

    try:
        with open(FILE_PATH, "r") as file_:
            return json.load(file_)

    except FileNotFoundError:
        create_todo_files()
        return []


def save(todos: dict) -> None:

    with open(FILE_PATH, "w+") as file_:
        json.dump(todos, file_)


def list_todos() -> None:

    for idx, todo in enumerate(load()):
        print(idx + 1, " - ", todo["description"], " - ", todo["status"].upper())


def add_todo(todo: str) -> None:
    todos = load()
    todos.append(
        {
            "description": todo,
            "status": "pending",
        }
    )
    save(todos)
    print(f"added: {todo}\n")


def remove_todo(idx: int) -> None:
    todos = load()

    if idx - 1 < 0 or idx > len(todos):
        print("invalid todo index\n")
        return

    todo = todos.pop(idx - 1)
    save(todos)
    print(f"removed: {todo['description']}\n")


def complete_todo(idx: int) -> None:
    todos = load()

    if idx - 1 < 0 or idx > len(todos):
        print("invalid todo index\n")
        return

    todos[idx - 1]["status"] = "completed"
    save(todos)
    print(f"completed: {todos[idx - 1]['description']}\n")


def main() -> None:

    # create parser
    parser = argparse.ArgumentParser()

    # add parser arguments
    parser.add_argument("-l", "--list", action="store_true", help="list all todos")
    parser.add_argument(
        "-a",
        "--add",
        dest="todo",
        type=str,
        action="store",
        help="add a new todo",
    )

    parser.add_argument(
        "-r",
        "--remove",
        dest="remove",
        type=int,
        action="store",
        help="remove a todo",
    )

    parser.add_argument(
        "-c",
        "--complete",
        dest="complete",
        type=int,
        action="store",
        help="complete a todo",
    )

    # parse args
    args = parser.parse_args(sys.argv[1:])

    # list todos
    if args.list:
        list_todos()

    # add todo
    elif args.todo:
        add_todo(args.todo)
        list_todos()

    # remove todo
    elif args.remove or args.remove == 0:
        remove_todo(args.remove)
        list_todos()

    # complete a todo
    elif args.complete or args.complete == 0:
        complete_todo(args.complete)
        list_todos()

    # otherwise print usage
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
