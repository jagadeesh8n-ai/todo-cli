#!/usr/bin/env python3
"""
todo.py — A simple command-line to-do list manager.

Usage:
    python todo.py add "Buy groceries"
    python todo.py list
    python todo.py done 1
    python todo.py remove 1
    python todo.py clear

Tasks are stored in a local JSON file (tasks.json) in the same directory.
"""

import json
import sys
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "tasks.json"


def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(description):
    tasks = load_tasks()
    tasks.append({"description": description, "done": False})
    save_tasks(tasks)
    print(f'Added: "{description}"')


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet. Add one with: python todo.py add \"Your task\"")
        return
    for i, task in enumerate(tasks, start=1):
        status = "x" if task["done"] else " "
        print(f"[{status}] {i}. {task['description']}")


def mark_done(index):
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        tasks[index - 1]["done"] = True
        save_tasks(tasks)
        print(f'Marked task {index} as done: "{tasks[index - 1]["description"]}"')
    else:
        print(f"No task with number {index}.")


def remove_task(index):
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        removed = tasks.pop(index - 1)
        save_tasks(tasks)
        print(f'Removed: "{removed["description"]}"')
    else:
        print(f"No task with number {index}.")


def clear_tasks():
    save_tasks([])
    print("All tasks cleared.")


def print_usage():
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "add" and len(sys.argv) >= 3:
        add_task(" ".join(sys.argv[2:]))
    elif command == "list":
        list_tasks()
    elif command == "done" and len(sys.argv) == 3:
        mark_done(int(sys.argv[2]))
    elif command == "remove" and len(sys.argv) == 3:
        remove_task(int(sys.argv[2]))
    elif command == "clear":
        clear_tasks()
    else:
        print_usage()


if __name__ == "__main__":
    main()
