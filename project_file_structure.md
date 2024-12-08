# Project Structure

```bash
game_api/
├── blueprints/                     # Contains route definitions
│   ├── user.py                     # User-related routes
│   └── utils.py                    # Utility functions for routes
│
├── controllers/                    # Contains the business logic
│   ├── user_controllers/           # Handles user-related actions
│   │   ├── user_controller_for_add_character.py
│   │   ├── user_controller_for_delete_character.py
│   │   ├── user_controller_for_edit_character.py
│   │   ├── user_controller_for_edit_user_profile.py
│   │   ├── user_controller_for_user_dashboard.py
│   │   ├── user_controller_for_view_character_list.py
│   │   └── user_controller_for_view_user_profile.py
│   └── common_fun.py               # Common functions for various actions
│
├── datamanager/                    # Manages data operations
│   ├── data_manager_interface.py   # Defines interface for data manager
│   └── PostgreSQLDataManager.py    # Implements PostgreSQL data operations
│
├── db/                             # Database setup and migration files
│   └── pgsql_script                # SQL scripts for database setup
│
├── migrations/                     # Alembic migration files
│   ├── versions/
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── static/                         # Static files (CSS, JS, images)
│   ├── CSS/
│   ├── fonts/
│   ├── icon-fonts/
│   ├── img/
│   ├── js/
│   └── sass/
│
├── templates/                      # HTML templates
│   ├── partials/                   # Reusable partials
│   ├── user/                       # User-related views
│   ├── 404.html                    # 404 error page
│   ├── contact.html                # Contact page
│   ├── index.html                  # Homepage
│   ├── login.html                  # Login page
│   └── signup.html                 # Signup page
│
├── tests/                          # Test files
│   ├── test_character.py           # Tests for character-related features
│   └── test_config.py              # Tests for configuration
│
├── .env                            # Environment variables
├── .gitignore                      # Git ignore file
├── characters.json                 # Sample character data
├── config.py                       # Application configuration
├── LICENSE                         # License information
├── models.py                       # Database models
├── project_file_structure          # Explanation of project structure
├── README.md                       # This file
├── requirements.txt                # Python dependencies
└── run.py                          # Entry point for the application
```