from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass(slots=True)
class MemoryItem:
    timestamp: str
    role: str
    content: str


class MemoryStore:
    """SQLite based short/long-term memory for conversations and actions."""

    def __init__(self, path: Path):
        self.path = path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL
                )
                """
            )

    def add(self, role: str, content: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO memory (timestamp, role, content) VALUES (?, ?, ?)",
                (datetime.utcnow().isoformat(), role, content),
            )

    def latest(self, limit: int = 8) -> Iterable[MemoryItem]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT timestamp, role, content FROM memory ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        for row in reversed(rows):
            yield MemoryItem(*row)
