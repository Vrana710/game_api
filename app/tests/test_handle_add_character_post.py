import os
import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from app.models import db, User, House, Role, Strength, Character
from flask import session
from dotenv import load_dotenv
from app.controllers.common_fun import user_logged_in

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class TestHandleAddCharacterPostSuccess(unittest.TestCase):
    """
    Test the handle_add_character_post function for success case.
    """

    def setUp(self):
        """Set up the test environment, create test data."""
        self.app = create_app()

        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
        self.app.config['SERVER_NAME'] = 'localhost:5000'
        self.app.config['APPLICATION_ROOT'] = '/'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        # Example test client initialization
        self.client = self.app.test_client(use_cookies=True)

        # Push the application context
        self.app_context = self.app.app_context()
        self.app_context.push()

    @patch('app.controllers.common_fun.User.query.get')
    @patch('app.controllers.common_fun.fetch_character_data')
    def test_handle_add_character_post_success(self, mock_fetch_character_data, mock_get):
        """
        Test the success flow of adding a character through handle_add_character_post.
        """
        with self.app.app_context():
            # Ensure the necessary data exists in the database
            self.house = House.query.filter_by(name='Gryffindor').first()
            if not self.house:
                self.house = House(name='Gryffindor')
                db.session.add(self.house)

            self.role = Role.query.filter_by(name='Wizard').first()
            if not self.role:
                self.role = Role(name='Wizard')
                db.session.add(self.role)

            self.strength = Strength.query.filter_by(name='Bravery').first()
            if not self.strength:
                self.strength = Strength(name='Bravery')
                db.session.add(self.strength)

            db.session.commit()  # Commit the changes to the database

        # Mock the character data to be fetched
        mock_fetch_character_data.return_value = {
            'name': 'Harry Potter',
            'house': self.house,
            'role': self.role,
            'strength': self.strength,
            'animal': 'Owl',
            'symbol': 'Lightning Bolt',
            'nickname': 'The Chosen One',
            'age': 17,
            'death': None
        }

        # Mock the user database call
        mock_user = MagicMock(User)
        mock_user.id = 16
        mock_user.email = 'test@gmail.com'  # Mock email
        mock_get.return_value = mock_user

        # Simulate login (no need to manually set session here)
        login_response = self.client.post('/auth/login', data={
            'email': 'test@gmail.com',
            'password': 'Test@1234'
        }, follow_redirects=True)

        # Check if the response is a redirect (302)
        self.assertEqual(login_response.status_code, 302)  # Expecting a redirect after login

        # Check if the redirect location is correct (e.g., home or dashboard)
        self.assertIn('/user/dashboard', login_response.location)  # Change this to your actual redirect URL

        # Set the user_id cookie manually in the test client after login
        with self.client.session_transaction() as session_data:
            session_data['user_id'] = 16  # Manually set user_id in the session

        # Now test adding a character
        response = self.client.post('/user/user_add_character', data={
            'name': 'Harry Potter',
            'house': self.house.id,  # Use the house ID, not the object
            'role': self.role.id,  # Use the role ID, not the object
            'strength': self.strength.id,  # Use the strength ID, not the object
            'animal': 'Owl',
            'symbol': 'Lightning Bolt',
            'nickname': 'The Chosen One',
            'age': 17,
            'death': None
        }, follow_redirects=True)

        # self.assertEqual(response.status_code, 302)
        # Ensure the response is correct
        self.assertEqual(response.status_code, 200)  # Ensure successful response

        # Check the redirect after successful character creation
        self.assertIn('/user/my_character_list', response.location)

        # Refetch the character and user in the session context
        with self.app.app_context():
            # Re-fetch the user and character
            user = User.query.get(16)  # Ensure to query the correct user ID
            character = Character.query.filter_by(name='Harry Potter').first()

            # Assert that the character was created successfully
            self.assertIsNotNone(character)
            self.assertEqual(character.name, 'Harry Potter')
            self.assertEqual(character.house.name, 'Gryffindor')
            self.assertEqual(character.role.name, 'Wizard')
            self.assertEqual(character.strength.name, 'Bravery')

        # Verify session is still active after the request
        with self.client.session_transaction() as session_data:
            self.assertEqual(session_data['user_id'], 16)


if __name__ == '__main__':
    unittest.main()
