from database.initializers import DatabaseInitializer
from interfaces.initializers import DataSourceInitializerInterface
from interfaces.repositories import UserRepositoryInterface
from interfaces.cli import UserCLIInterface
from interfaces.services import UserServiceInterface

from repositories.users import UserRepository
from services.users import UserService
from cli.user_commands import UserCLI


class DependencyContainer:
    """
    A simple dependency injection container for managing project dependencies.

    Attributes:
        _db_name (str): Name of the SQLite database file.
        _user_repository (UserRepository): User repository instance.
        _user_cli (UserCLI): CLI instance for user interactions.
        _database_initializer (DatabaseInitializer): Database initializer instance.
        user_service (UserService): Service instance for managing user logic.
    """

    def __init__(self, db_name: str) -> None:
        """
        Initializes the DependencyContainer with a given database name.

        Args:
            db_name (str): The name of the SQLite database file.
        """
        self._db_name = db_name

        self._database_initializer = self._init_database_initializer()
        self._user_repository = self._init_user_repository()
        self._user_cli = self._init_user_cli()
        self.user_service = self._init_user_service()

    def _init_database_initializer(self) -> DataSourceInitializerInterface:
        """
        Initializes the database initializer.

        Returns:
            DatabaseInitializer: An instance of the DatabaseInitializer.
        """
        return DatabaseInitializer(self._db_name)

    def _init_user_repository(self) -> UserRepositoryInterface:
        """
        Initializes the user repository.

        Returns:
            UserRepository: An instance of the UserRepository.
        """
        return UserRepository(self._db_name)

    def _init_user_cli(self) -> UserCLIInterface:
        """
        Initializes the CLI for user interactions.

        Returns:
            UserCLI: An instance of the UserCLI.
        """
        return UserCLI()

    def _init_user_service(self) -> UserServiceInterface:
        """
        Initializes the user service.

        Returns:
            UserService: An instance of the UserService.
        """
        return UserService(self._user_repository, self._user_cli)

    @property
    def database_initializer(self) -> DataSourceInitializerInterface:
        """
        Provides access to the database initializer.

        Returns:
            DatabaseInitializer: The database initializer instance.
        """
        return self._database_initializer
