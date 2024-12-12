"""
=============================================================================
Project: Game API App
Developer: Varsha Rana
File: test_handle_not_logged_in.py
Description:
The `test_handle_not_logged_in.py` file defines the test suite for handling cases where users are not logged in and attempt to access restricted areas of the Game API App. It tests the behavior of the application when a user is not authenticated, ensuring they are redirected to the login page. The test checks that the application correctly handles unauthorized access attempts by using redirection.

Key Features:
1. **Not Logged In Handling**:
   - **Redirection**: Verifies that the user is redirected to the login page when they attempt to access a restricted area without being logged in.

2. **Test Setup**:
   - Sets up the application in test mode and simulates the request context for the test.
   - Uses the `patch` decorator to mock the `redirect` and `url_for` functions, ensuring proper redirection behavior.

3. **Application Context**:
   - Ensures the application context is set up correctly for the test, allowing for accurate simulation of user interaction.

Created: 2024-12-09
Updated: 2024-12-09
=============================================================================
"""

import os
import unittest
from unittest.mock import patch
from app import create_app  # Assuming you have a function to create your app
from app.controllers.common_fun import handle_not_logged_in
from dotenv import load_dotenv

load_dotenv()


class TestHandleNotLoggedIn(unittest.TestCase):

    @patch('app.controllers.common_fun.redirect')
    @patch('app.controllers.common_fun.url_for')
    def test_handle_not_logged_in_redirect(self, mock_url_for, mock_redirect):
        # Create app instance and push request context
        app = create_app()  # Ensure this function creates your Flask app
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URL")
        app.config['SERVER_NAME'] = 'localhost:5000'  # or your domain/host
        app.config['APPLICATION_ROOT'] = '/'  # The root path of your application
        # Ensure the app is in test mode
        app.config['TESTING'] = True
        with app.test_request_context():  # Simulate a request context for the test
            # Simulate not logged in
            mock_url_for.return_value = '/login'
            mock_redirect.return_value = '/login'

            result = handle_not_logged_in()
            mock_redirect.assert_called_once_with('/login')
            self.assertEqual(result, '/login')


if __name__ == '__main__':
    unittest.main()
