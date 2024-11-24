from abc import ABC, abstractmethod


class UserServiceInterface(ABC):

    @abstractmethod
    def create_user(self) -> None:
        """
        Handles the creation of a user. Interacts with the CLI for input and repository for data storage.

        If an `IncorrectUserData` error is raised, prompts the user to retry or exit.
        """

    @abstractmethod
    def get_user(self) -> None:
        """
        Retrieves a user's data by their email. Interacts with the CLI for input and repository for data retrieval.

        If the user is not found, displays an error message and asks whether to retry.
        """

    @abstractmethod
    def get_all_users(self) -> None:
        """
        Retrieves all users from the repository and displays them using the CLI.
        """

    @abstractmethod
    def update_user(self) -> None:
        """
        Handles the update of a user's data.
        Interacts with the CLI for input and repository for data storage.

        If an error occurs, displays the error message and asks whether to retry.
        """

    @abstractmethod
    def delete_user(self) -> None:
        """
        Handles the deletion of a user by email.
        Interacts with the CLI for input and repository for data deletion.

        If an error occurs, displays the error message and asks whether to retry.
        """

    @abstractmethod
    def delete_all_users(self) -> None:
        """
        Handles the deletion of all users from the database.
        Prompts for confirmation before performing the action.
        """
