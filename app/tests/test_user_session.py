"""=============================================================================
Project: Game API App
Developer: Varsha Rana
File: test_user_session.py
Description:
The `test_user_session.py` file defines the test suite for handling user session management within the Game API App. It tests the behavior of the application when checking if a user is logged in by querying the session for the user ID and matching it to the database. The tests ensure that the application properly identifies when a user is logged in or not, based on session data.

Key Features:
1. **User Session Management**:
   - **Logged In**: Verifies that the application correctly identifies a logged-in user by checking the session for a valid user ID and retrieving user data from the database.
   - **Not Logged In**: Ensures that the application correctly handles the case where the session does not contain a valid user ID, returning `None` to indicate that no user is logged in.

2. **Test Setup**:
   - Sets up the Flask app in test mode and simulates request contexts for testing.
   - Mocks the database call to retrieve user data and patches the Flask session to simulate logged-in and non-logged-in states.

3. **Application Context**:
   - Ensures that the application context is correctly pushed and popped around tests, allowing for accurate simulation of user interactions.

Created: 2024-12-09
Updated: 2024-12-09
=============================================================================
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from flask import session

from app import create_app  # Ensure this function creates your Flask app
from app.controllers.common_fun import user_logged_in
from app.models import User
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class TestUserSession(unittest.TestCase):
    def setUp(self):
        """Set up the Flask app and push the app context."""
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URL")
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Push the application context
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Pop the application context."""
        self.app_context.pop()

    @patch('app.controllers.common_fun.User.query.get')
    def test_user_logged_in_logged_in(self, mock_get):
        # Mock the user database call
        mock_user = MagicMock(User)
        mock_user.id = 1
        mock_get.return_value = mock_user

        # Patch the Flask session
        with self.app.test_request_context():
            session['user_id'] = 1

            # Call the function
            user = user_logged_in()
            self.assertIsNotNone(user)
            self.assertEqual(user.id, 1)

    @patch('app.controllers.common_fun.User.query.get')
    def test_user_logged_in_not_logged_in(self, mock_get):
        # Mock the user database call
        mock_get.return_value = None

        # Clear the Flask session
        with self.app.test_request_context():
            session.clear()

            # Call the function
            user = user_logged_in()
            self.assertIsNone(user)


if __name__ == '__main__':
    unittest.main()
