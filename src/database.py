import re
import sqlite3
from typing import Optional
from dataclasses import dataclass

DB_NAME = 'users.sqlite'


@dataclass(kw_only=True, frozen=True)
class UserBaseValueObject:
    """
    Base Value Object for user-related data.

    Attributes:
        name (str): The first name of the user.
        surname (str): The last name of the user.
        age (int): The age of the user, must be between 18 and 100.
    """
    name: str
    surname: str
    age: int

    def __post_init__(self) -> None:
        """
        Initializes the UserBaseValueObject with validations and normalizations.

        Validates:
        - The types of the fields.
        - The age range.
        Normalizes:
        - The name and surname to lowercase.
        """
        self.check_type(self.name, str, "name")
        self.check_type(self.surname, str, "surname")
        self.check_type(self.age, int, "age")

        if not (18 <= self.age <= 100):
            raise ValueError("Age must be between 18 and 100")

        object.__setattr__(self, "name", self.name.lower())
        object.__setattr__(self, "surname", self.surname.lower())

    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validates and normalizes an email address.

        Args:
            email (str): The email address to validate.

        Returns:
            str: The normalized (lowercase) email address.

        Raises:
            ValueError: If the email address is invalid.
        """
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            raise ValueError(f"Invalid email address: {email}")
        return email.lower()

    @staticmethod
    def check_type(value: int | str, expected_type: type[int] | type[str], field_name: str) -> None:
        """
        Checks that a value is of the expected type.

        Args:
            value (int | str): The value to check.
            expected_type (type[int] | type[str]): The expected type of the value.
            field_name (str): The name of the field for error reporting.

        Raises:
            TypeError: If the value is not of the expected type.
        """
        if not isinstance(value, expected_type):
            raise TypeError(f"{field_name} must be of type {expected_type.__name__}, got {type(value).__name__}")

    def as_dict(self) -> dict:
        """
        Converts the dataclass instance to a dictionary.

        Returns:
            dict: A dictionary representation of the dataclass.
        """
        return {field: value for field, value in vars(self).items()}


@dataclass(kw_only=True, frozen=True)
class UserCreateUpdateVO(UserBaseValueObject):
    """
    Value Object for creating or updating a user.

    Attributes:
        email (str): The email address of the user.
    """
    email: str

    def __post_init__(self) -> None:
        """
        Initializes the UserCreateUpdateVO with validations and normalizations.

        Validates:
        - The type of the email.
        - The format of the email.
        Normalizes:
        - The email to lowercase.
        """
        super().__post_init__()

        self.check_type(self.email, str, "email")

        normalized_email = UserBaseValueObject.validate_email(self.email)
        object.__setattr__(self, "email", normalized_email)


@dataclass(kw_only=True, frozen=True)
class UserVO(UserBaseValueObject):
    """
    Value Object representing a user with an ID.

    Attributes:
        id (int): The unique identifier of the user.
        email (str): The email address of the user.
    """
    id: int
    email: str

    def __post_init__(self) -> None:
        """
        Initializes the UserVO with validations and normalizations.

        Validates:
        - The type of the ID and email.
        - The ID is a positive integer.
        - The format of the email.
        Normalizes:
        - The email to lowercase.
        """
        super().__post_init__()

        self.check_type(self.id, int, "id")
        self.check_type(self.email, str, "email")

        if self.id <= 0:
            raise ValueError("ID must be a positive integer")

        normalized_email = UserBaseValueObject.validate_email(self.email)
        object.__setattr__(self, "email", normalized_email)


class DatabaseInitializer:
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


class UserRepository:
    """
    Class for CRUD operations on the users table.

    Attributes:
        _db_name (str): The name of the SQLite database file.
    """

    def __init__(self, db_name: str) -> None:
        """
        Initializes the repository with the database name.

        Args:
            db_name (str): The name of the SQLite database file.
        """
        self._db_name = db_name

    def add_user(self, new_user: UserCreateUpdateVO) -> UserVO:
        """
        Adds a new user to the database and returns their UserVO representation.

        Args:
            new_user (UserCreateUpdateVO): The user data to add.

        Returns:
            UserVO: The created user's value object, including their new ID.
        """
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO users (email, name, surname, age) 
            VALUES (?, ?, ?, ?)
        """, (new_user.email, new_user.name, new_user.surname, new_user.age))
        user_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        connection.close()
        return UserVO(
            id=user_id,
            **new_user.as_dict()
        )

    def get_user_by_email(self, email: str) -> Optional[UserVO]:
        """
        Retrieves a user's data by their email.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            Optional[UserVO]: The user's value object, or None if the user is not found.
        """
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, email, name, surname, age
            FROM users
            WHERE email = ?
        """, (email,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        if not row:
            return None
        return UserVO(
            id=row[0],
            email=row[1],
            name=row[2],
            surname=row[3],
            age=row[4]
        )

    def get_all_users(self) -> list[UserVO]:
        """
        Retrieves all users from the database.

        Returns:
            list[UserVO]: A list of value objects representing all users in the database.
        """
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, email, name, surname, age
            FROM users
        """)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return [
            UserVO(
                id=row[0],
                email=row[1],
                name=row[2],
                surname=row[3],
                age=row[4]
            )
            for row in rows
        ]

    def update_user(self, user_to_update: UserCreateUpdateVO) -> None:
        """
        Updates a user's data in the database.

        Args:
            user_to_update (UserCreateUpdateVO): The updated user data, identified by their email.
        """
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE users
            SET name = ?, surname = ?, age = ?
            WHERE email = ?
        """, (user_to_update.name, user_to_update.surname, user_to_update.age, user_to_update.email))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_user_by_email(self, email: str) -> None:
        """
        Deletes a user from the database by their email.

        Args:
            email (str): The email address of the user to delete.
        """
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM users
            WHERE email = ?
        """, (email,))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_all_users(self) -> None:
        """
        Deletes all users from the database.
        """
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM users
        """)
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == '__main__':
    db_initializer = DatabaseInitializer(DB_NAME)
    db_initializer.initialize_table()

    user_repository = UserRepository(DB_NAME)

    user_data = UserCreateUpdateVO(
        email='john_doe@example.com',
        name='john',
        surname='doe',
        age=25
    )

    # user_repository.delete_all_users()
    # new_user = user_repository.add_user(user_data)
    # print(f'New user: {new_user}')

    user = user_repository.get_user_by_email(user_data.email)
    print(f'Get user: {user}')

    users = user_repository.get_all_users()
    print(f'All users: {users}')

    user_data_updated = UserCreateUpdateVO(
        email='john_doe@example.com',
        name='john',
        surname='doe',
        age=35
    )

    user_repository.update_user(user_data_updated)

    user = user_repository.get_user_by_email(user_data.email)
    print(f'Get updated user: {user}')


