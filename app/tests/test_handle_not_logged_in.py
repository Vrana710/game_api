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
