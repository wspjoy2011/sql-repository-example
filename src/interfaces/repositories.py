from abc import ABC, abstractmethod

from domain.vo.users import UserCreateUpdateVO, UserVO


class UserRepositoryInterface(ABC):
    """
    Interface for class for CRUD operations on the users table.
    """

    @abstractmethod
    def add_user(self, new_user: UserCreateUpdateVO) -> UserVO:
        """
        Adds a new user to the database and returns their UserVO representation.

        Args:
            new_user (UserCreateUpdateVO): The user data to add.

        Returns:
            UserVO: The created user's value object, including their new ID.
        """

    @abstractmethod
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

    @abstractmethod
    def get_all_users(self) -> list[UserVO]:
        """
        Retrieves all users from the database.

        Returns:
            list[UserVO]: A list of value objects representing all users in the database.
        """

    def update_user(self, user_to_update: UserCreateUpdateVO) -> None:
        """
        Updates a user's data in the database.

        Args:
            user_to_update (UserCreateUpdateVO): The updated user data, identified by their email.

        Raises:
            UserNotFound: If the user with the given email does not exist.
        """

    def delete_user_by_email(self, email: str) -> None:
        """
        Deletes a user from the database by their email.

        Args:
            email (str): The email address of the user to delete.

        Raises:
            UserNotFound: If the user with the given email does not exist.
        """

    @abstractmethod
    def delete_all_users(self) -> None:
        """
        Deletes all users from the database.
        """
