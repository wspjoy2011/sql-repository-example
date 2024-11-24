from dependencies.users import DependencyContainer
from settings.config import DB_NAME


def print_help(commands: dict) -> None:
    """
    Prints the list of available commands and their descriptions.

    Args:
        commands (dict): A dictionary of commands and their metadata.
    """
    print("\nAvailable commands:")
    for command, meta in commands.items():
        print(f"  {command}: {meta['description']}")
    print()


def user_management_cli(db_name: str) -> None:
    """
    Command-line interface for user management.

    Args:
        db_name (str): The name of the SQLite database file.
    """
    user_container = DependencyContainer(db_name)
    user_container.database_initializer.initialize_table()
    user_service = user_container.user_service

    commands = {
        "create": {
            "func": user_service.create_user,
            "description": "Create a new user in the database.",
        },
        "get": {
            "func": user_service.get_user,
            "description": "Retrieve a user's details by their email.",
        },
        "list": {
            "func": user_service.get_all_users,
            "description": "List all users in the database.",
        },
        "update": {
            "func": user_service.update_user,
            "description": "Update an existing user's details.",
        },
        "delete": {
            "func": user_service.delete_user,
            "description": "Delete a user by their email.",
        },
        "delete_all": {
            "func": user_service.delete_all_users,
            "description": "Delete all users from the database.",
        },
        "help": {
            "func": lambda: print_help(commands),
            "description": "Show the list of available commands and their descriptions.",
        },
    }

    print("Welcome to users application.\n")
    print("Type 'help' to see the list of available commands.\n")

    while True:
        print("Enter command")
        user_command = input(">>> ").strip().lower()

        if user_command in commands:
            func = commands[user_command]["func"]
            func()
        elif user_command == "exit":
            print("Exiting")
            break
        else:
            print("Unsupported command! Type 'help' to see the list of commands.\n")

if __name__ == '__main__':
    user_management_cli(DB_NAME)

