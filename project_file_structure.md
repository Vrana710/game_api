# Project Structure

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