import sqlite3
from sqlite3 import IntegrityError

from domain.vo.users import UserCreateUpdateVO, UserVO
from exceptions.users import IncorrectUserData, UserNotFound
from interfaces.repositories import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
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

        Raises:
            IncorrectUserData: If the user data violates database constraints (e.g., duplicate email).
        """
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (email, name, surname, age) 
                VALUES (?, ?, ?, ?)
            """, (new_user.email, new_user.name, new_user.surname, new_user.age))
            user_id = cursor.lastrowid
            connection.commit()
        except IntegrityError as e:
            raise IncorrectUserData(f"Failed to add user: {e}")
        finally:
            cursor.close()
            connection.close()

        return UserVO(
            id=user_id,
            **new_user.as_dict()
        )

    def get_user_by_email(self, email: str) -> UserVO:
        """
        Retrieves a user's data by their email.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            UserVO: The user's value object.

        Raises:
            UserNotFound: If no user with the given email is found.
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
            raise UserNotFound(f"User with email {email} not found.")

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

        Raises:
            UserNotFound: If the user with the given email does not exist.
        """
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE users
                SET name = ?, surname = ?, age = ?
                WHERE email = ?
            """, (user_to_update.name, user_to_update.surname, user_to_update.age, user_to_update.email))

            if cursor.rowcount == 0:
                raise UserNotFound(f"User with email {user_to_update.email} not found.")

            connection.commit()
        except IntegrityError as e:
            raise IncorrectUserData(f"Failed to add user: {e}")
        finally:
            cursor.close()
            connection.close()

    def delete_user_by_email(self, email: str) -> None:
        """
        Deletes a user from the database by their email.

        Args:
            email (str): The email address of the user to delete.

        Raises:
            UserNotFound: If the user with the given email does not exist.
        """
        connection = sqlite3.connect(self._db_name)
        cursor = connection.cursor()
        try:
            cursor.execute("""
                DELETE FROM users
                WHERE email = ?
            """, (email,))

            if cursor.rowcount == 0:
                raise UserNotFound(f"User with email {email} not found.")

            connection.commit()
        finally:
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
