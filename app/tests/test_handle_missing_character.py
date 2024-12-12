"""
=============================================================================
Project: Game API App
Developer: Varsha Rana
File: test_handle_missing_character.py
Description:
The `test_handle_missing_character.py` file defines the test suite for handling the case when a character's name is missing during the update process in the Game API App. It tests the behavior of the application when a character name is required but not provided. The test ensures that the application correctly triggers a flash message indicating the error.

Key Features:
1. **Missing Character Name Handling**:
   - **Flash Message**: Verifies that a flash message is shown when the character name is missing, indicating the error to the user.
   - **Error Handling**: Ensures the application gracefully handles missing character information with appropriate user feedback.

2. **Test Setup**:
   - Sets up the application in test mode and pushes the application context for the test.
   - Uses the `patch` decorator to mock the `flash` function and assert that it is called with the expected error message.

3. **Application Context**:
   - The test ensures that the application context is properly set up and that the necessary configurations are loaded for testing.

Created: 2024-12-09
Updated: 2024-12-09
=============================================================================
"""

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
