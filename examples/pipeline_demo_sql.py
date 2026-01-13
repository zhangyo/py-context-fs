import os
import sqlite3
import sys
from typing import Any, Dict, List, Optional

# Ensure the package is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from py_context_fs.core import ContextFile, ContextRouter, ContextSource
from py_context_fs.pipeline import ContextConstructor, ContextLoader


class SQLResolver(ContextSource):
    """SQLite-backed resolver for simple note records."""

    def __init__(self, db_path: str):
        self._db_path = db_path
        self._init_db()

    def read(self, path: str, view: str = "default") -> ContextFile:
        note_id = self._parse_id(path)
        column = "summary" if view == "summary" else "content"
        row = self._query_one(
            f"SELECT id, {column} FROM notes WHERE id = ?", (note_id,)
        )
        if not row or row[1] is None:
            raise FileNotFoundError(f"Note not found: {path} (view={view})")
        return ContextFile(content=row[1], metadata={"id": row[0], "view": view})

    def list(self, path: str) -> List[str]:
        if path not in ("", ".", "/"):
            return []
        rows = self._query_all("SELECT id FROM notes ORDER BY id")
        return [f"{row[0]}.txt" for row in rows]

    def search(self, query: str) -> List[str]:
        rows = self._query_all(
            "SELECT id FROM notes WHERE content LIKE ? OR summary LIKE ? ORDER BY id",
            (f"%{query}%", f"%{query}%"),
        )
        return [f"{row[0]}.txt" for row in rows]

    def write(
        self, path: str, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        note_id = self._parse_id(path)
        summary = None
        if metadata and "summary" in metadata:
            summary = metadata["summary"]
        self._execute(
            """
            INSERT INTO notes (id, content, summary)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET content=excluded.content, summary=excluded.summary
            """,
            (note_id, content, summary),
        )

    def _parse_id(self, path: str) -> int:
        name = path.strip("/").split("/")[-1]
        if name.endswith(".txt"):
            name = name[:-4]
        if not name.isdigit():
            raise ValueError(f"Invalid note path: {path}")
        return int(name)

    def _init_db(self) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY,
                    content TEXT NOT NULL,
                    summary TEXT
                )
                """
            )
            conn.commit()

    def _execute(self, query: str, params: tuple) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(query, params)
            conn.commit()

    def _query_one(self, query: str, params: tuple) -> Optional[tuple]:
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(query, params)
            return cur.fetchone()

    def _query_all(self, query: str, params: tuple = ()) -> List[tuple]:
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(query, params)
            return cur.fetchall()


def main():
    print("Initializing SQL-backed demo...")

    db_path = os.path.join(os.path.dirname(__file__), "sql_demo.db")
    resolver = SQLResolver(db_path)

    resolver.write(
        "1.txt",
        "This is a detailed note about Agentic File Systems and pipelines.",
        metadata={"summary": "AFS overview note."},
    )
    resolver.write(
        "2.txt",
        "This note covers token budgeting and summary fallbacks.",
        metadata={"summary": "Token budgeting note."},
    )

    fs = ContextRouter()
    fs.mount("/db", resolver)

    constructor = ContextConstructor(fs)
    manifest = constructor.construct(paths=["/db/1.txt", "/db/2.txt"])

    loader = ContextLoader(fs)
    context = loader.load(manifest, max_tokens=120)

    print("\n[Generated Context START]")
    print(context)
    print("[Generated Context END]\n")

    print("List:")
    print(fs.list("/db"))
    print("Search for 'token':")
    print(fs.search("token"))
    print("Read summary view for /db/2.txt:")
    print(fs.open("/db/2.txt", view="summary").content)


if __name__ == "__main__":
    main()
