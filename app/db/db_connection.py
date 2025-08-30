import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os

class DatabaseManager:
    def __init__(self):
        self.connection = None
        # Get connection string from environment variable
        self.connection_string = os.getenv('DATABASE_URL')
        if not self.connection_string:
            raise ValueError("DATABASE_URL environment variable is required")
    
    def connect(self):
        """Initialize the database connection"""
        if self.connection is None or self.connection.closed:
            self.connection = psycopg2.connect(self.connection_string)
            self.connection.autocommit = False
        return self.connection
    
    def close(self):
        """Close the database connection"""
        if self.connection and not self.connection.closed:
            self.connection.close()
    
    @contextmanager
    def get_cursor(self, commit=True):
        """Context manager for database operations"""
        conn = self.connect()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def execute_query(self, query, params=None, commit=True):
        """Execute a query with parameters"""
        with self.get_cursor(commit=commit) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_insert(self, query, params=None):
        """Execute an insert query"""
        with self.get_cursor(commit=True) as cursor:
            cursor.execute(query, params)
            return cursor.rowcount

# Global database manager instance
db_manager = DatabaseManager()

