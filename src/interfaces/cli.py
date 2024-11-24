from abc import ABC, abstractmethod

from domain.vo.users import UserCreateUpdateVO, UserVO


class UserCLIInterface(ABC):
    """
    Interface for class to handle user management operations via command-line interface.
    """

    @classmethod
    @abstractmethod
    def create_user(cls) -> UserCreateUpdateVO:
        """
        Prompts the user to input data and creates a UserCreateUpdateVO.

        Returns:
            UserCreateUpdateVO: A value object containing the user data.

        Raises:
            IncorrectUserData: If the input data is invalid.
        """

    @classmethod
    @abstractmethod
    def get_email(cls) -> str:
        """
        Prompts the user to input an email address.

        Returns:
            str: The email address entered by the user.

        Raises:
            IncorrectUserData: If the input email is empty or invalid.
        """

    @classmethod
    @abstractmethod
    def get_all(cls, users: list[UserVO]) -> None:
        """
        Displays all users in a formatted table.

        Args:
            users (list[UserVO]): A list of user value objects.
        """

    @classmethod
    @abstractmethod
    def update_user(cls) -> UserCreateUpdateVO:
        """
        Prompts the user to input an email and update the user's data.

        Returns:
            UserCreateUpdateVO: A value object containing the updated user data.

        Raises:
            IncorrectUserData: If the input data is invalid.
        """

    @classmethod
    @abstractmethod
    def delete_all(cls) -> bool:
        """
        Prompts the user for confirmation before deleting all users.

        Returns:
            bool: True if the user confirms deletion, False otherwise.
        """

    @classmethod
    @abstractmethod
    def ask_retry(cls) -> bool:
        """
        Asks the user if they want to retry the operation.

        Returns:
            bool: True if the user wants to retry, False to exit.
        """

