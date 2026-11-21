"""List pantry batches in earliest-expiry order."""

import argparse
import sqlite3
from contextlib import closing
from datetime import date


def iso_date(text):
    return date.fromisoformat(text).isoformat()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="pantry-datebook.sqlite3", help="SQLite database path")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List records")
    command = commands.add_parser("store", help="Add a dated batch.")
    command.add_argument("food")
    command.add_argument("expires", type=iso_date)
    command = commands.add_parser("used", help="Remove a finished batch.")
    command.add_argument("food")
    command.add_argument("expires", type=iso_date)
    args = parser.parse_args()
    try:
        with closing(sqlite3.connect(args.db)) as db, db:
            db.execute("CREATE TABLE IF NOT EXISTS items (food TEXT, expires TEXT, PRIMARY KEY(food, expires))")
            if args.command == "list":
                for row in db.execute("SELECT expires, food FROM items ORDER BY 1, 2"):
                    print(" | ".join(map(str, row)))
            elif args.command == "store":
                db.execute("INSERT INTO items VALUES (?, ?)", (args.food, args.expires))
            elif args.command == "used":
                if not db.execute("DELETE FROM items WHERE food=? AND expires=?", (args.food, args.expires)).rowcount:
                    raise ValueError("Batch not found")
    except (ValueError, sqlite3.Error) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
