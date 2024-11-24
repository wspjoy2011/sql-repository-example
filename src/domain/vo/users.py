import re
from dataclasses import dataclass


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
