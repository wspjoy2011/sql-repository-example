# User Management Application

This is a simple user management application built with Python. It allows users to create, retrieve, update, delete, and list users via a command-line interface (CLI). The project is self-contained and does not require any external dependencies.

---

## Project Structure

```plaintext
.
├── cli
│   ├── __init__.py                 # CLI package initializer
│   └── user_commands.py            # CLI logic for user commands
├── database
│   ├── __init__.py                 # Database package initializer
│   └── initializers.py             # Database table initialization logic
├── dependencies
│   ├── __init__.py                 # Dependency container initializer
│   └── users.py                    # Dependency container for user-related services
├── domain
│   ├── __init__.py                 # Domain logic package initializer
│   └── vo                          # Value objects for data modeling
│       ├── __init__.py             
│       └── users.py                # User value objects (VO)
├── exceptions
│   ├── __init__.py                 # Exceptions package initializer
│   └── users.py                    # Custom exceptions for user management
├── interfaces
│   ├── __init__.py                 # Interfaces package initializer
│   ├── cli.py                      # Interface definitions for CLI
│   ├── initializers.py             # Interface definitions for database initialization
│   ├── repositories.py             # Interface definitions for repository operations
│   └── services.py                 # Interface definitions for service logic
├── main.py                         # Entry point of the application
├── repositories
│   ├── __init__.py                 # Repositories package initializer
│   └── users.py                    # User repository for CRUD operations
├── services
│   ├── __init__.py                 # Services package initializer
│   └── users.py                    # User service logic
├── settings
│   ├── __init__.py                 # Settings package initializer
│   └── config.py                   # Application configuration
```

---

## Features

1. **User Management**:
   - Create, retrieve, update, delete, and list users.
   - Store user data in an SQLite database.
2. **CLI Interface**:
   - Interact with the application via simple commands.
3. **Self-Contained**:
   - No external dependencies required.

---

## Installation and Setup

### Step 1: Install Python
Ensure you have Python 3.10+ installed on your system. You can download the latest version of Python from [python.org](https://www.python.org/downloads/).

### Step 2: Set Up a Virtual Environment (Optional)
It is recommended to use a virtual environment to isolate the project.

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

### Step 3: Run the Application
1. Initialize the SQLite database and start the CLI:
   ```bash
   python main.py
   ```
2. Follow the on-screen instructions to interact with the application.

---

## Commands in CLI

| Command       | Description                              |
|---------------|------------------------------------------|
| `create`      | Create a new user.                      |
| `get`         | Retrieve a user's details by their email.|
| `list`        | List all users in the database.         |
| `update`      | Update an existing user's details.      |
| `delete`      | Delete a user by their email.           |
| `delete_all`  | Delete all users from the database.     |
| `help`        | Show the list of available commands.    |
| `exit`        | Exit the application.                   |

---

## Example Usage

### Create a User
```plaintext
Enter command
>>> create
Enter email: john.doe@example.com
Enter name: John
Enter surname: Doe
Enter age: 25
User john.doe@example.com successfully created.
```

### List All Users
```plaintext
Enter command
>>> list
----------------------------------------
| ID  | Email               | Name     | Surname  | Age  |
----------------------------------------
| 1   | john.doe@example.com| John     | Doe      | 25   |
----------------------------------------
```

### Update a User
```plaintext
Enter command
>>> update
Enter email: john.doe@example.com
Enter the updated details:
Enter new name: Johnathan
Enter new surname: Doe
Enter new age: 30
User john.doe@example.com successfully updated.
```

### Delete a User
```plaintext
Enter command
>>> delete
Enter email: john.doe@example.com
User with email john.doe@example.com successfully deleted.
```

---

## Contribution
Contributions are welcome! Feel free to fork the repository and submit a pull request.

---

## License
This project is open-source and available under the MIT License.