import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os
from typing import Optional

class DatabaseManager:
    _instance: Optional['DatabaseManager'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.connection = None
            self.connection_string = None
            self._initialized = True
    
    def initialize(self, connection_string: str):
        """Initialize the database manager with connection string"""
        if self.connection_string is None:
            self.connection_string = connection_string
        else:
            raise RuntimeError("DatabaseManager already initialized")
    
    def connect(self):
        """Initialize the database connection"""
        if not self.connection_string:
            raise RuntimeError("DatabaseManager not initialized. Call initialize() first.")
        
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

def get_db_manager() -> DatabaseManager:
    """Factory function to get the database manager instance"""
    return DatabaseManager()
