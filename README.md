# Game API

Game API is a web-based platform that allows users to manage characters, edit profiles, and interact with others through a series of dynamic and responsive features. This project uses Flask and PostgreSQL to provide a seamless experience for users to manage their character lists, profile details, and more.

## Table of Contents
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Running the Application](#running-the-application)
- [API Routes](#api-routes)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

To run this project locally, follow the steps below:

1. Clone the repository:
   ```bash
   git clone https://github.com/Vrana710/game_api.git
   ```

2. Navigate to the project directory:
   ```bash
   cd game_api
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables in the `.env` file, ensuring the database credentials are correct:
   ```
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key
   ```

5. Apply database migrations:
   ```bash
   * Initialize migrations: flask db init
   * Create a migration script: flask db migrate -m "Initial migration"
   * Apply the migration: flask db upgrade
   ```

6. Run the application:
   ```bash
   python run.py
   ```

## Project Structure

```bash
game_api/
├── app/  
│    ├── blueprints/                     # Contains route definitions
│    │   ├── auth.py                     # User-Authentication-related routes
│    │   ├── user.py                     # User-related routes
│    │   └── utils.py                    # Utility functions for routes
│    │
│    ├── controllers/                    # Contains the business logic
│    │   ├── auth_controllers/           # Handles user-related Authentication actions
│    │   │   ├── auth_controller_for_login.py
│    │   │   └── auth_controller_for_logout.py
│    │   ├── user_controllers/           # Handles user-related actions
│    │   │   ├── user_controller_for_add_character.py
│    │   │   ├── user_controller_for_delete_character.py
│    │   │   ├── user_controller_for_edit_character.py
│    │   │   ├── user_controller_for_edit_user_profile.py
│    │   │   ├── user_controller_for_user_dashboard.py
│    │   │   ├── user_controller_for_view_character_list.py
│    │   │   └── user_controller_for_view_user_profile.py
│    │   ├── common_fun.py               # Common functions for various actions
│    │   ├── contact_controller.py       # Contact logic
│    │   └── signup_user_controller.py   # Signup User Logic
│    │
│    ├── datamanager/                    # Manages data operations
│    │   ├── data_manager_interface.py   # Defines interface for data manager
│    │   └── PostgreSQLDataManager.py    # Implements PostgreSQL data operations
│    │
│    ├── db/                             # Database setup and migration files
│    │   └── pgsql_script                # SQL scripts for database setup
│    │
│    ├── migrations/                     # Alembic migration files
│    │   ├── versions/
│    │   ├── alembic.ini
│    │   ├── env.py
│    │   ├── README
│    │   └── script.py.mako
│    │
│    ├── static/                         # Static files (CSS, JS, images)
│    │   ├── CSS/
│    │   ├── fonts/
│    │   ├── icon-fonts/
│    │   ├── img/
│    │   ├── js/
│    │   └── sass/
│    │
│    ├── templates/                      # HTML templates
│    │   ├── partials/                   # Reusable partials
│    │   ├── user/                       # User-related views
│    │   ├── 404.html                    # 404 error page
│    │   ├── contact.html                # Contact page
│    │   ├── index.html                  # Homepage
│    │   ├── login.html                  # Login page
│    │   └── signup.html                 # Signup page
│    │
│    ├── tests/                          # Test files
│    │   ├── test_character.py           # Tests for character-related features
│    │   └── test_config.py              # Tests for configuration
│    ├── __init.py                       # Initializes configures its core components
│    ├── characters.json                 # Sample character data
│    └── models.py                       # Database models
├── .env                            # Environment variables
├── .gitignore                      # Git ignore file
├── config.py                       # Application configuration
├── LICENSE                         # License information
├── project_file_structure          # Explanation of project structure
├── README.md                       # This file
├── requirements.txt                # Python dependencies
└── run.py                          # Entry point for the application
```

## Features

- **User Registration & Login:** Allows users to create an account and log in.
- **Character Management:** Users can add, edit, and delete characters.
- **Profile Management:** Users can view and edit their profiles.
- **User Dashboard:** A personalized dashboard displaying user information and characters.
- **Database Integration:** PostgreSQL used for data persistence.

## Technologies Used

- **Flask:** Web framework for Python.
- **PostgreSQL:** Relational database for data storage.
- **Alembic:** Database migration tool.
- **SQLAlchemy:** ORM for database interactions.
- **Jinja2:** Templating engine for rendering HTML.

## Running the Application

To start the application:

1. Make sure PostgreSQL is running and the database is set up.
2. Run the application using:
   ```bash
   python run.py
   ```
3. Visit `http://localhost:5000` in your browser.

## API Routes

### Home
- **Route**: `/`
- **Methods**: `GET`
- **Description**: Displays the home page of the app.

### Contact Form
- **Route**: `/contact`
- **Methods**: `GET`, `POST`
- **Description**: 
    - `GET`: Displays the contact form.
    - `POST`: Submits the contact form and saves the contact details to the database. It flashes a success or error message based on the form submission result.

### User Signup
- **Route**: `/signup_user`
- **Methods**: `GET`, `POST`
- **Description**: 
    - `GET`: Displays the user registration form.
    - `POST`: Handles the user signup process by validating the form, hashing the password, uploading the profile picture, and saving the new user in the database. Returns a success message or an error if the email already exists.

### User Login
- **Route**: `/login`
- **Methods**: `GET`, `POST`
- **Description**:
    - `GET`: Displays the login form.
    - `POST`: Handles the user login by verifying the email/username and password. If successful, it stores the user ID in the session and redirects to the user dashboard. If authentication fails, it shows an error message.

### User Logout
- **Route**: `/logout`
- **Methods**: `GET`
- **Description**: Logs the user out by clearing the session and redirects to the login page. Also prevents caching to ensure the session is fully cleared.

### Cache Clearing
- **Route**: `/clear_cache`
- **Methods**: `GET`
- **Description**: Clears the cache if the user is authenticated (through JWT, as implied in the original code). If the cache clearing is successful, a flash message is shown. If not, a warning message is displayed.

### Error Handling - 404 Not Found
- **Route**: `/404`
- **Methods**: `GET`
- **Description**: A custom error handler that renders a 404 error page if the requested route is not found.

### User Dashboard
- **Route**: `/dashboard`
- **Methods**: `GET`
- **Description**: Displays the user's dashboard with relevant information and statistics.

### Character List
- **Route**: `/character_list`
- **Methods**: `GET`
- **Description**: Retrieves and displays the list of characters available to the user.

### Add Character
- **Route**: `/add_character`
- **Methods**: `GET`, `POST`
- **Description**: Displays the form for adding a new character (GET) or processes the form submission (POST) to add a character.

### Edit Character
- **Route**: `/edit_character/<int:character_id>`
- **Methods**: `GET`, `POST`
- **Description**: Displays the form for editing an existing character (GET) or processes the form submission (POST) to update character details. The character is identified by `character_id`.

### Delete Character
- **Route**: `/delete_character/<int:character_id>`
- **Methods**: `POST`
- **Description**: Deletes the specified character identified by `character_id`. The action requires a POST request to confirm deletion.

### User Profile
- **Route**: `/user_profile`
- **Methods**: `GET`
- **Description**: Displays the user's profile information.

### Edit User Profile
- **Route**: `/edit_user_profile/<int:user_id>`
- **Methods**: `GET`, `POST`
- **Description**: Displays the form for editing a user's profile (GET) or processes the form submission (POST) to update the profile. The user is identified by `user_id`.


## Testing

The project includes comprehensive unit tests to ensure the functionality of the Game API. Below is an overview of the testing process, including test strategies, tools used, and instructions on how to run the tests.

### Comprehensive Unit Testing

Unit tests are developed for all API endpoints using the `pytest` framework. The tests validate the correct behavior for each operation, including all CRUD (Create, Read, Update, Delete) actions. Each API endpoint is tested to ensure:

- Correct handling of valid requests.
- Proper response status codes (e.g., `200 OK`, `201 Created`, `404 Not Found`).
- Accurate data returned in the response body.
- Edge cases and invalid inputs are correctly handled.

### Edge Case Coverage

The tests cover a variety of edge cases, ensuring that the API handles invalid inputs and error conditions properly. These tests include:

- **Invalid Data Formats:** Test cases that send data in incorrect formats (e.g., incorrect data types or malformed JSON).
- **Missing or Extra Fields:** Validate that requests with missing or extra fields are handled appropriately.
- **Incorrect HTTP Methods:** Ensure that unsupported HTTP methods (e.g., `PUT` for a `GET` endpoint) return the correct status code (`405 Method Not Allowed`).
- **Nonexistent Character IDs:** Test for attempts to access or modify characters that do not exist in the database, ensuring the API returns a `404 Not Found` status.

Tests also verify the robustness of error handling, ensuring that appropriate status codes (`400 Bad Request`, `404 Not Found`, etc.) and error messages are returned in all failure scenarios.

### Mocking & Dependency Management

To avoid reliance on external systems (such as databases or external APIs), the tests utilize tools like `unittest.mock` or `pytest-mock` to simulate external dependencies and database interactions. This allows for precise control over the test conditions and ensures that the tests remain fast and isolated.

Mocking is used to simulate:

- Database interactions, ensuring that tests do not require a live database.
- External API calls, preventing the tests from relying on third-party services.

By mocking dependencies, we ensure that the unit tests are focused solely on the behavior of the application, without external factors influencing the test results.

### Validation Testing

Validation rules are tested for both creating and updating characters. The tests ensure that the API enforces the necessary data constraints, such as:

- **Required Fields:** Ensure all mandatory fields are provided in the request body (e.g., character name, description).
- **Correct Data Types:** Validate that each field contains the correct data type (e.g., strings for names, integers for age).
  
Additionally, the filtering and sorting mechanisms are thoroughly tested:

- **Case-Insensitive Filtering and Sorting:** Ensure that the filtering and sorting operations on character lists are case-insensitive and work as expected (e.g., `Character` and `character` should be treated the same).
- **Special Characters Handling:** Test that the system handles special characters (e.g., `@`, `#`, `&`) in both filtering and sorting operations.
- **Empty Results Handling:** Ensure that requests with no matching results return the correct empty response (e.g., `[]` with a `200 OK` status).

### Documentation

To run the tests and interpret the results, follow these steps:

1. **Install Dependencies**: Ensure you have all the necessary testing dependencies installed by running:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Tests**: To run the test suite, use the following command:
   ```bash
   pytest
   
   python3 -m pytest --cov=game_api --cov-report=html
   ```

   This will automatically discover and run all the test cases in the `tests` directory. If you wish to run specific tests, you can specify the test file or test function:
   ```bash
    python3 -m pytest tests/test_character.py
   python3 -m pytest tests/test_config.py
   ```

3. **Interpreting Results**: After running the tests, `pytest` will provide a summary of the test results. If all tests pass, the output will indicate `X passed in Y seconds`. If any tests fail, `pytest` will show detailed information about the failure, including the error message and the failing test case.

4. **Dependencies for Testing**: Ensure the following dependencies are installed for testing:
   - `pytest`: For running the test suite.
   - `pytest-mock`: For mocking external dependencies.
   - `unittest`: Built-in testing framework for Python.

### Test Coverage Analysis

We use `pytest-cov` to generate a test coverage report, which shows how much of the code is covered by tests. To generate a coverage report, run the following command:

```bash
pytest --cov=game_api --cov-report=html
```

This will generate an HTML report in the `htmlcov/` directory, which you can open in your browser to view detailed coverage information.

**Interpreting Coverage Report**:
- The report provides an overview of the percentage of code covered by the tests.
- Aim for a high percentage of coverage, especially for critical code paths such as user authentication, character creation, and database interactions.
- You can also analyze which specific lines or functions are not covered and improve your tests accordingly.

By using `pytest-cov`, we ensure that our tests cover a significant portion

 of the application and that potential issues are identified early.

## Contributing

We welcome contributions to this project. To contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and commit them.
4. Push to your forked repository.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
