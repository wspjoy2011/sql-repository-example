from domain.vo.users import UserCreateUpdateVO, UserVO
from exceptions.users import IncorrectUserData
from interfaces.cli import UserCLIInterface


class UserCLI(UserCLIInterface):
    """
    A class to handle user management operations via command-line interface.
    """

    @classmethod
    def create_user(cls) -> UserCreateUpdateVO:
        """
        Prompts the user to input data and creates a UserCreateUpdateVO.

        Returns:
            UserCreateUpdateVO: A value object containing the user data.

        Raises:
            IncorrectUserData: If the input data is invalid.
        """
        try:
            email = input("Enter email: ").strip().lower()
            name = input("Enter name: ").strip().capitalize()
            surname = input("Enter surname: ").strip().capitalize()
            age = int(input("Enter age: ").strip())

            user_vo = UserCreateUpdateVO(
                email=email,
                name=name,
                surname=surname,
                age=age
            )

            return user_vo

        except (ValueError, TypeError) as e:
            raise IncorrectUserData(f"Invalid input: {e}")

        except Exception as e:
            raise IncorrectUserData(f"An error occurred: {e}")

    @classmethod
    def get_email(cls) -> str:
        """
        Prompts the user to input an email address.

        Returns:
            str: The email address entered by the user.

        Raises:
            IncorrectUserData: If the input email is empty or invalid.
        """
        while True:
            email = input("Enter email: ").strip().lower()
            if email:
                return email
            else:
                print("Email cannot be empty. Please try again.")

    @classmethod
    def get_all(cls, users: list[UserVO]) -> None:
        """
        Displays all users in a formatted table.

        Args:
            users (list[UserVO]): A list of user value objects.
        """
        if not users:
            print("No users found.")
            return

        headers = ["ID", "Email", "Name", "Surname", "Age"]

        column_widths = [
            max(len(headers[0]), max(len(str(user.id)) for user in users)),
            max(len(headers[1]), max(len(user.email) for user in users)),
            max(len(headers[2]), max(len(user.name) for user in users)),
            max(len(headers[3]), max(len(user.surname) for user in users)),
            max(len(headers[4]), max(len(str(user.age)) for user in users)),
        ]

        header_row = " | ".join(f"{header:<{width}}" for header, width in zip(headers, column_widths))
        separator_row = "-+-".join("-" * width for width in column_widths)
        print(separator_row)
        print(header_row)
        print(separator_row)

        for user in users:
            user_row = " | ".join(
                f"{str(value):<{width}}"
                for value, width in zip(
                    [user.id, user.email, user.name, user.surname, user.age],
                    column_widths
                )
            )
            print(user_row)
        print(separator_row)

    @classmethod
    def update_user(cls) -> UserCreateUpdateVO:
        """
        Prompts the user to input an email and update the user's data.

        Returns:
            UserCreateUpdateVO: A value object containing the updated user data.

        Raises:
            IncorrectUserData: If the input data is invalid.
        """
        try:
            email = input("Enter the email of the user to update: ").strip().lower()

            print("Enter the updated details:")
            name = input("Enter new name: ").strip().capitalize()
            surname = input("Enter new surname: ").strip().capitalize()
            age = int(input("Enter new age: ").strip())

            user_vo = UserCreateUpdateVO(
                email=email,
                name=name,
                surname=surname,
                age=age
            )

            return user_vo

        except (ValueError, TypeError) as e:
            raise IncorrectUserData(f"Invalid input: {e}")

        except Exception as e:
            raise IncorrectUserData(f"An error occurred: {e}")

    @classmethod
    def delete_all(cls) -> bool:
        """
        Prompts the user for confirmation before deleting all users.

        Returns:
            bool: True if the user confirms deletion, False otherwise.
        """
        while True:
            confirmation = input(
                "Are you sure you want to delete all users? This action cannot be undone. (yes/no): "
            ).strip().lower()

            if confirmation in ["yes", "y"]:
                return True
            elif confirmation in ["no", "n"]:
                print("Action canceled.")
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    @classmethod
    def ask_retry(cls) -> bool:
        """
        Prompts the user to decide whether to retry the operation or exit.

        Returns:
            bool: True if the user wants to retry, False to exit.
        """
        while True:
            user_input = input("Do you want to retry? (yes/no): ").strip().lower()
            if user_input in ["yes", "y"]:
                return True
            elif user_input in ["no", "n"]:
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

