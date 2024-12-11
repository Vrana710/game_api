import os
import unittest
from unittest.mock import patch
from app import create_app  # Assuming you have a function to create your app
from app.controllers.common_fun import handle_missing_character_name
from dotenv import load_dotenv

load_dotenv()


class TestHandleMissingCharacterName(unittest.TestCase):

    @patch('app.controllers.common_fun.flash')
    def test_handle_missing_character_name(self, mock_flash):
        # Create app instance and push application context
        app = create_app()  # Ensure this function creates your Flask app
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URL")
        app.config['SERVER_NAME'] = 'localhost:5000'  # or your domain/host
        app.config['APPLICATION_ROOT'] = '/'  # The root path of your application
        # Ensure the app is in test mode
        app.config['TESTING'] = True
        with app.app_context():  # Push application context for the test
            # Simulate missing character name
            handle_missing_character_name()
            mock_flash.assert_called_with('Character name is required!', 'danger')


if __name__ == '__main__':
    unittest.main()
