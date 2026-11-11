#!/usr/bin/env python3
"""Tiny todo CLI. Tasks live in todos.json next to this file."""
import argparse
import json
import os
import sys

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos.json")


def load():
    if not os.path.exists(DB):
        return []
    with open(DB, encoding="utf-8") as f:
        return json.load(f)


def save(tasks):
    with open(DB, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def cmd_add(args):
    tasks = load()
    tasks.append({"id": (tasks[-1]["id"] + 1 if tasks else 1), "text": args.text, "done": False})
    save(tasks)
    print("Added:", args.text)


def cmd_list(args):
    tasks = load()
    if not tasks:
        print("No todos yet.")
        return
    for t in tasks:
        mark = "x" if t["done"] else " "
        print("[%s] %d %s" % (mark, t["id"], t["text"]))


def cmd_done(args):
    tasks = load()
    for t in tasks:
        if t["id"] == args.id:
            t["done"] = True
            save(tasks)
            print("Done:", t["text"])
            return
    print("No todo with id", args.id, file=sys.stderr)
    sys.exit(1)


def cmd_clear(args):
    save([t for t in load() if not t["done"]])
    print("Cleared finished todos.")


def main():
    p = argparse.ArgumentParser(prog="todo")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("text")
    a.set_defaults(fn=cmd_add)
    li = sub.add_parser("list")
    li.set_defaults(fn=cmd_list)
    d = sub.add_parser("done")
    d.add_argument("id", type=int)
    d.set_defaults(fn=cmd_done)
    c = sub.add_parser("clear")
    c.set_defaults(fn=cmd_clear)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
