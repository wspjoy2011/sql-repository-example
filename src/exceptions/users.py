class IncorrectUserData(Exception):
    """
    Exception raised when user data provided via CLI is incorrect.
    """
    def __init__(self, message: str):
        super().__init__(message)

class UserNotFound(Exception):
    """
    Exception raised when a user is not found in the database.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
