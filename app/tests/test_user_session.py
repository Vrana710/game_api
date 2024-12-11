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
