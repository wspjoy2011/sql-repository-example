from abc import ABC, abstractmethod


class DataSourceInitializerInterface(ABC):
    """Interface for class to initialize the users table in the database."""

    @abstractmethod
    def initialize_table(self) -> None:
        """Creates the users table if it does not exist."""
