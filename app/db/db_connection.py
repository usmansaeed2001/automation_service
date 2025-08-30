import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager
from typing import Optional, Iterable, Any


class DatabaseManager:
    _instance: Optional['DatabaseManager'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.connection: Optional[psycopg.Connection] = None
            self.connection_string: Optional[str] = None
            self._initialized = True

    def initialize(self, connection_string: str):
        """Initialize the database manager with connection string."""
        if self.connection_string is None:
            self.connection_string = connection_string
        else:
            raise RuntimeError("DatabaseManager already initialized")

    def connect(self) -> psycopg.Connection:
        """Initialize (or return) the psycopg v3 connection."""
        if not self.connection_string:
            raise RuntimeError("DatabaseManager not initialized. Call initialize() first.")

        if self.connection is None or self.connection.closed:
            # dict_row makes cursor fetches return dicts (RealDictCursor-equivalent)
            self.connection = psycopg.connect(self.connection_string, row_factory=dict_row)
            self.connection.autocommit = False  # explicit transactions like before
        return self.connection

    def close(self):
        """Close the database connection."""
        if self.connection and not self.connection.closed:
            self.connection.close()

    @contextmanager
    def get_cursor(self, commit: bool = True):
        """
        Context manager for DB operations.
        - Opens a cursor on a live connection.
        - Commits on success if `commit=True`, otherwise leaves TX open.
        - Rolls back on exception and re-raises.
        """
        conn = self.connect()
        cur = conn.cursor()
        try:
            yield cur
            if commit:
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    def execute_query(self, query: str, params: Optional[Iterable[Any]] = None, commit: bool = True):
        """
        Execute a query and return all rows (as list[dict]).
        Note: Use this for SELECT/CTE returning rows. Non-returning queries will raise on fetch.
        """
        with self.get_cursor(commit=commit) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_insert(self, query: str, params: Optional[Iterable[Any]] = None) -> int:
        """
        Execute an INSERT/UPDATE/DELETE and return affected row count.
        """
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(query, params)
            return cursor.rowcount


def get_db_manager() -> DatabaseManager:
    """Factory function to get the database manager instance."""
    return DatabaseManager()
