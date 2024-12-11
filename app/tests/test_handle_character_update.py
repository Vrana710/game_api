import os
import uuid
import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from app.models import db, User, House, Role, Strength, Character
from flask import session
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class TestHandleCharacterUpdatePostSuccess(unittest.TestCase):
    """
    Test the handle_character_update_post function for success case.
    """

    def setUp(self):
        """Set up the test environment, create test data."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URL")
        self.app.config['SERVER_NAME'] = 'localhost:5000'
        self.app.config['APPLICATION_ROOT'] = '/'
        self.app.config['TESTING'] = True

        # Set up the application context
        with self.app.app_context():
            unique_username = f"test_user_{uuid.uuid4().hex[:8]}"
            unique_email = f"{unique_username}@example.com"
            self.user = User(
                username=unique_username,
                email=unique_email,
                password='Test@1234',
                date_of_birth='1992-10-10',
                gender='male',
                profile_picture='test.jpeg',
                created_at=datetime.now(),
                updated_at=datetime.now())
            db.session.add(self.user)
            db.session.commit()

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

            # Create a test character
            self.character = Character(
                name='Harry Potter',
                house=self.house,
                role=self.role,
                strength=self.strength,
                user_id=self.user.id
            )
            db.session.add(self.character)
            db.session.commit()

            db.session.commit()

    # def tearDown(self):
    #     """Clean up after each test."""
    #     with self.app.app_context():
    #         db.session.remove()
    #         db.drop_all()

    @patch('app.controllers.common_fun.fetch_character_data')
    def test_handle_character_update_post_success(self, mock_fetch_character_data):
        """
        Test the success flow of updating a character through handle_character_update_post.
        """

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

        # Log in as the test user
        with self.client.session_transaction() as session_data:
            session_data['user_id'] = self.user.id  # Ensure the user is logged in

        # Make a POST request to update the character
        response = self.client.post(f'/user/edit_character/{self.character.id}', data={
            'name': 'Harry Potter Updated',
            'house': self.house,
            'role': self.role,
            'strength': self.strength,
            'animal': 'Owl',
            'symbol': 'Lightning Bolt',
            'nickname': 'The Chosen One',
            'age': 17,
            'death': None
        })

        # Check for a 302 status code (redirect to character list)
        self.assertEqual(response.status_code, 302)
        # Check the redirect location to confirm it's correct
        self.assertIn('/user/my_character_list', response.location)

        # Refetch the character in the session context to avoid detached instance
        with self.app.app_context():
            # Re-fetch the user and character
            user = User.query.get(self.user.id)
            character = Character.query.filter_by(name='Harry Potter Updated').first()

            # Assert that the character was updated successfully
            self.assertIsNotNone(character)
            self.assertEqual(character.name, 'Harry Potter Updated')
            self.assertEqual(character.house.name, 'Gryffindor')
            self.assertEqual(character.role.name, 'Wizard')
            self.assertEqual(character.strength.name, 'Bravery')

        # Verify session is still active after the request
        with self.client.session_transaction() as session_data:
            self.assertEqual(session_data['user_id'], self.user.id)


if __name__ == '__main__':
    unittest.main()
