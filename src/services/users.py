from exceptions.users import IncorrectUserData, UserNotFound
from interfaces.cli import UserCLIInterface
from interfaces.repositories import UserRepositoryInterface
from interfaces.services import UserServiceInterface


class UserService(UserServiceInterface):
    def __init__(self, repository: UserRepositoryInterface, cli: UserCLIInterface) -> None:
        self._repository = repository
        self._cli = cli

    def create_user(self) -> None:
        """
        Handles the creation of a user. Interacts with the CLI for input and repository for data storage.

        If an `IncorrectUserData` error is raised, prompts the user to retry or exit.
        """
        while True:
            try:
                user_vo = self._cli.create_user()
                self._repository.add_user(user_vo)
                print(f"User {user_vo.email} successfully created.")
                break

            except IncorrectUserData as e:
                print(f"Error: {e}")

                if not self._cli.ask_retry():
                    print("Exiting the user creation menu.")
                    break

    def get_user(self) -> None:
        """
        Retrieves a user's data by their email. Interacts with the CLI for input and repository for data retrieval.

        If the user is not found, displays an error message and asks whether to retry.
        """
        while True:
            try:
                email = self._cli.get_email()
                user = self._repository.get_user_by_email(email)
                print(f"User found: {user}")
                break

            except UserNotFound as e:
                print(f"Error: {e}")

                if not self._cli.ask_retry():
                    print("Exiting the user retrieval menu.")
                    break

    def get_all_users(self) -> None:
        """
        Retrieves all users from the repository and displays them using the CLI.
        """
        users = self._repository.get_all_users()
        self._cli.get_all(users)

    def update_user(self) -> None:
        """
        Handles the update of a user's data.
        Interacts with the CLI for input and repository for data storage.

        If an error occurs, displays the error message and asks whether to retry.
        """
        while True:
            try:
                updated_user_vo = self._cli.update_user()  # Get updated user data from CLI
                self._repository.update_user(updated_user_vo)  # Update user in repository
                print(f"User {updated_user_vo.email} successfully updated.")
                break
            except UserNotFound as e:
                print(f"Error: {e}")
                if not self._cli.ask_retry():
                    print("Exiting the update menu.")
                    break
            except IncorrectUserData as e:
                print(f"Error: {e}")
                if not self._cli.ask_retry():
                    print("Exiting the update menu.")
                    break

    def delete_user(self) -> None:
        """
        Handles the deletion of a user by email.
        Interacts with the CLI for input and repository for data deletion.

        If an error occurs, displays the error message and asks whether to retry.
        """
        while True:
            try:
                email = self._cli.get_email()  # Get email from CLI
                self._repository.delete_user_by_email(email)  # Delete user in repository
                print(f"User with email {email} successfully deleted.")
                break
            except UserNotFound as e:
                print(f"Error: {e}")
                if not self._cli.ask_retry():
                    print("Exiting the deletion menu.")
                    break

    def delete_all_users(self) -> None:
        """
        Handles the deletion of all users from the database.
        Prompts for confirmation before performing the action.
        """
        if self._cli.delete_all():
            self._repository.delete_all_users()
            print("All users have been successfully deleted.")
