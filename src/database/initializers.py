import sqlite3

from interfaces.initializers import DataSourceInitializerInterface


class DatabaseInitializer(DataSourceInitializerInterface):
    """Class to initialize the users table in the database."""

    def __init__(self, db_name: str) -> None:
        self._db_name = db_name

    def initialize_table(self) -> None:
        """Creates the users table if it does not exist."""
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL CHECK (LENGTH(email) <= 100 AND email LIKE '%_@__%.__%'),
                name TEXT NOT NULL CHECK (LENGTH(name) <= 50),
                surname TEXT NOT NULL CHECK (LENGTH(surname) <= 50),
                age INTEGER NOT NULL CHECK (age BETWEEN 18 AND 100)
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
