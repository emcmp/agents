import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "crews.db"
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("➡️  Tables:")
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in cur.fetchall():
    print(" -", row["name"])

print("\n➡️  Agents:")
for row in conn.execute("SELECT * FROM agent"):
    print(dict(row))

print("\n➡️  Crew:")
for row in conn.execute("SELECT * FROM crew"):
    print(dict(row))

print("\n➡️  Tasks:")
for row in conn.execute("SELECT * FROM task"):
    print(dict(row))

print("\n➡️  CrewTask:")
for row in conn.execute("SELECT * FROM crew_task"):
    print(dict(row))

conn.close()
