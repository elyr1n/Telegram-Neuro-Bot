import sqlite3

from pathlib import Path

DB_PATH = Path("users.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER UNIQUE,
                first_name TEXT,
                last_name TEXT,
                username TEXT
            );

            CREATE TABLE IF NOT EXISTS users_in_ban (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER UNIQUE
            );
            
            CREATE TABLE IF NOT EXISTS chat_context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                role TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES users(chat_id)
            );
            """
        )
        conn.commit()

    print("База данных инициализирована!")


def add_user(
    chat_id: int,
    first_name: str | None,
    last_name: str | None,
    username: str | None,
):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO users (chat_id, first_name, last_name, username)
            VALUES (?, ?, ?, ?)
            """,
            (chat_id, first_name, last_name, "@" + username if username else None),
        )
        conn.commit()


def ban_user(chat_id: int):
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO users_in_ban (chat_id) VALUES (?)", (chat_id,)
        )
        conn.commit()


def unban_user(chat_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM users_in_ban WHERE chat_id = ?", (chat_id,))
        conn.commit()


def is_user_banned(chat_id: int) -> bool:
    with get_connection() as conn:
        result = conn.execute(
            "SELECT 1 FROM users_in_ban WHERE chat_id = ? LIMIT 1",
            (chat_id,),
        ).fetchone()

    return result is not None


def add_to_context(chat_id: int, role: str, content: str):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO chat_context (chat_id, role, content)
            VALUES (?, ?, ?)
            """,
            (chat_id, role, content),
        )
        conn.commit()


def get_context(chat_id: int, limit: int = 10) -> list:
    with get_connection() as conn:
        messages = conn.execute(
            """
            SELECT role, content 
            FROM chat_context 
            WHERE chat_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
            """,
            (chat_id, limit),
        ).fetchall()

        return list(reversed(messages))


def clear_context(chat_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM chat_context WHERE chat_id = ?", (chat_id,))
        conn.commit()
