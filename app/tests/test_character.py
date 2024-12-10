"""=============================================================================
Project: Game API App
Developer: Varsha Rana
File: test_character.py
Description:
    This file contains unit tests for the Game API App, focusing on
    the `Character` entity. The tests ensure the proper functioning of
    CRUD operations (Create, Read, Update, Delete) for characters, validating
    both the API endpoints and database interactions.

    Key Features Tested:
    - Adding a new character.
    - Retrieving character details.
    - Updating existing character data.
    - Deleting characters.
    - Handling invalid or missing input during character creation.
    - Verifying behavior when accessing non-existent characters.

    The application leverages Flask for API development and SQLAlchemy
    for ORM-based database interactions. Test configurations utilize
    a separate test database for isolated and reliable test results.

    The `pytest` framework is employed for test automation, with fixtures
    to manage app context, database setup/teardown, and sample data creation.

Created: 2024-12-02
Updated: 2024-12-09
=============================================================================
"""
import os
import uuid
import pytest
from flask import url_for
from app import create_app
from app.models import db, Character
from dotenv import load_dotenv
from app.blueprints.utils import fetch_character_data

# Ensure the correct path
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


@pytest.fixture
def app():
    """Fixture to create and configure the app for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URL")
    app.config['SERVER_NAME'] = 'localhost:5000'  # or your domain/host
    app.config['APPLICATION_ROOT'] = '/'  # The root path of your application

    # Initialize the database inside the app context
    with app.app_context():
        db.create_all()  # Create tables before the tests run
    yield app  # Return the app instance for use in tests


@pytest.fixture
def client(app):
    """Fixture for the test client."""
    return app.test_client()


# Fixture for setting up and tearing down the database
@pytest.fixture
def init_db(app):
    with app.app_context():
        db.create_all()  # Set up the database before tests
        yield db
        db.drop_all()  # Tear down the database after tests


@pytest.fixture
def sample_character(app, logged_in_user):
    """Fixture to create a sample character associated with the logged-in user."""
    with app.app_context():
        character = Character(
            name="Test Character",
            animal="Dragon",
            symbol="Fire",
            nickname="Testy",
            age=30,
            user_id=logged_in_user.id  # Ensure this is the logged-in user's ID
        )
        db.session.add(character)
        db.session.commit()
        print(f"DEBUG: Created character: {character}")  # Debug output
        return character


@pytest.fixture
def logged_in_user(client, app):
    """Fixture to create and log in a user for testing."""
    with app.app_context():
        from app.models import User
        unique_username = f"test_user_{uuid.uuid4().hex[:8]}"
        unique_email = f"{unique_username}@example.com"

        test_user = User(username=unique_username, email=unique_email)
        test_user.set_password("testing@gmail.com")
        db.session.add(test_user)
        db.session.commit()

        response = client.post(url_for('auth_bp.login'), data={
            'email': unique_email,
            'password': 'testing@gmail.com'
        }, follow_redirects=True)

        assert response.status_code == 200

        return test_user


def test_add_character_from_json(client, app, logged_in_user):
    """Test adding a character using only the name, fetching other details from characters.json."""
    with app.app_context():
        # Use the name of the character to fetch data
        character_name = "Jon Snow"
        character_data = fetch_character_data(character_name)

        assert character_data is not None, f"Character '{character_name}' not found in characters.json"

        # Use only the name for the POST request
        response = client.post(
            url_for('user_bp.user_add_character'),
            json={"name": character_data['name']},  # Send only the name
            headers={'Content-Type': 'application/json'},
            follow_redirects=True
        )

        # Assertions
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
        data = response.get_json()
        assert data is not None, "Expected JSON response but got None"

        # Validate database entry
        db_character = Character.query.filter_by(name=character_data['name']).first()
        assert db_character is not None, "Character not found in the database"
        assert db_character.name == character_data['name'], "Database: Name mismatch"
        assert db_character.animal == character_data['animal'], "Database: Animal mismatch"
        assert db_character.symbol == character_data['symbol'], "Database: Symbol mismatch"
        assert db_character.nickname == character_data['nickname'], "Database: Nickname mismatch"
        assert db_character.age == character_data['age'], "Database: Age mismatch"


def test_get_character(client, app, logged_in_user, sample_character):
    """Test retrieving a character by checking the list of all characters."""
    with app.app_context():
        # Fetch all characters with JSON request
        response = client.get(
            url_for('user_bp.my_character_list'),
            headers={'Accept': 'application/json'}
        )
        assert response.status_code == 200, "Expected status code 200"

        # Debug: Print the raw response data Delete this after is working
        data = response.get_json()
        print("\nDEBUG: Response data:", data)

        assert isinstance(data, list), "Expected a list of characters in response"

        # Iterate to find the sample character
        found_character = next(
            (char for char in data if char['name'] == "Test Character"), None
        )

        assert found_character is not None, ("Sample character not "
                                             "found in character list")
        assert found_character[
                   'name'] == sample_character.name, (f"Expected name '{sample_character.name}', "
                                                      f"got '{found_character['name']}'")
        assert found_character[
                   'animal'] == sample_character.animal, (f"Expected animal '{sample_character.animal}', "
                                                          f"got '{found_character['animal']}'")
        assert found_character[
                   'symbol'] == sample_character.symbol, (f"Expected symbol '{sample_character.symbol}', "
                                                          f"got '{found_character['symbol']}'")
        assert found_character[
                   'nickname'] == sample_character.nickname, (f"Expected nickname '{sample_character.nickname}', "
                                                              f"got '{found_character['nickname']}'")
        assert found_character[
                   'age'] == sample_character.age, (f"Expected age '{sample_character.age}', "
                                                    f"got '{found_character['age']}'")
        assert found_character[
                   'id'] == sample_character.id, (f"Expected id '{sample_character.id}', "
                                                  f"got '{found_character['id']}'")


def test_update_character(client, app, logged_in_user, sample_character):
    """Test updating a character."""
    with app.app_context():
        # Simulate a form submission to update the character
        response = client.post(
            url_for('user_bp.user_edit_character',
                    character_id=sample_character.id),
            data={
                'name': 'Updated Character',
                'animal': 'Griffin',
                'symbol': 'Wind',
                'nickname': 'Griffy',
                'age': 35
            },
            follow_redirects=True
        )
        assert response.status_code == 200, (f"Expected status code 200, "
                                             f"got {response.status_code}")

        # Verify the database reflects the updates
        updated_character = Character.query.get(sample_character.id)
        assert updated_character is not None, "Character not found in the database"
        assert updated_character.name == 'Updated Character', "Database: Name update failed"
        assert updated_character.animal == 'Griffin', "Database: Animal update failed"
        assert updated_character.symbol == 'Wind', "Database: Symbol update failed"
        assert updated_character.nickname == 'Griffy', "Database: Nickname update failed"
        assert updated_character.age == 35, "Database: Age update failed"


def test_delete_character(client, app, logged_in_user,
                          sample_character):
    """Test deleting a character."""
    with app.app_context():
        response = client.post(
            url_for('auth_bp.login'),
            data={
                'email': logged_in_user.email,
                'password': 'testing@gmail.com'
            },
            follow_redirects=True
        )
        assert response.status_code == 200, "Failed to log in"

        response = client.post(
            url_for('user_bp.delete_character',
                    character_id=sample_character.id),
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 302, (f"Expected status code 302, "
                                             f"got {response.status_code}")

        deleted_character = Character.query.get(sample_character.id)
        assert deleted_character is None, ("Character was not deleted from "
                                           "the database")


def test_invalid_character_creation(client, app, logged_in_user):
    """Test invalid character creation (missing required fields)."""
    with app.app_context():
        response = client.post(
            url_for('user_bp.user_add_character'),
            json={
                'name': ''  # Missing required fields (e.g., 'name')
            },
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 400, (f"Expected status code 400, "
                                             f"got {response.status_code}")

        data = response.get_json()
        assert 'error' in data, "Expected 'error' in response JSON"
        assert data[
                   'error'] == 'Character name is required', (f"Expected error 'Character name is required', "
                                                              f"got {data['error']}")


def test_character_not_found_in_list(client, app, logged_in_user):
    """Test ensuring a non-existent character is not in the character list."""
    with app.app_context():  # Add application context
        # Fetch the list of characters
        response = client.get(
            url_for('user_bp.my_character_list'),
            headers={'Accept': 'application/json'}
        )
        assert response.status_code == 200, (f"Expected status code 200, "
                                             f"got {response.status_code}")

        data = response.get_json()
        assert isinstance(data, list), "Expected a list of characters in response"

        found_character = next((char for char in data if char['id'] == 9999), None)
        assert found_character is None, ("Non-existent character should"
                                         " not be found in the list")
