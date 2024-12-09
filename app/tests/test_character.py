import os
import pytest
from flask import url_for
from app import create_app
from app.models import db, Character
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')  # Ensure the correct path
load_dotenv(dotenv_path)


@pytest.fixture
def app():
    """Fixture to create and configure the app for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URL")

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
def sample_character(app):
    """Fixture to create a sample character."""
    with app.app_context():
        character = Character(
            name="Test Character",
            animal="Dragon",
            symbol="Fire",
            nickname="Testy",
            age=30
        )
        db.session.add(character)
        db.session.commit()
    return character


def test_create_character(client, app):
    """Test creating a character."""
    with app.app_context():  # Ensure the app context is active
        response = client.post(url_for('user_bp.user_add_character'), json={
            'name': 'New Character',
            'animal': 'Phoenix',
            'symbol': 'Flame',
            'nickname': 'Flamy',
            'age': 25
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['name'] == 'New Character'
        assert data['animal'] == 'Phoenix'
        assert data['symbol'] == 'Flame'
        assert data['nickname'] == 'Flamy'
        assert data['age'] == 25


def test_get_character(client, sample_character, app):
    """Test retrieving a character."""
    with app.app_context():
        # Make sure the object is still part of the session
        db.session.refresh(sample_character)

        response = client.get(url_for('user_bp.my_character_list',
                                      character_id=sample_character.id))
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == sample_character.id
        assert data['name'] == sample_character.name
        assert data['animal'] == sample_character.animal
        assert data['symbol'] == sample_character.symbol
        assert data['nickname'] == sample_character.nickname
        assert data['age'] == sample_character.age


def test_update_character(client, sample_character):
    """Test updating a character."""
    response = client.put(url_for('user_bp.user_edit_character',
                                  character_id=sample_character.id),
                          json={
        'name': 'Updated Character',
        'animal': 'Griffin',
        'symbol': 'Wind',
        'nickname': 'Griffy',
        'age': 35
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Character'
    assert data['animal'] == 'Griffin'
    assert data['symbol'] == 'Wind'
    assert data['nickname'] == 'Griffy'
    assert data['age'] == 35


def test_delete_character(client, sample_character, app):
    """Test deleting a character."""
    with app.app_context():
        db.session.delete(sample_character)
        # Commit the session to finalize the_delete
        db.session.commit()

        response = client.delete(url_for('user_bp.delete_character',
                                         character_id=sample_character.id))
        assert response.status_code == 204

        # Check if character is actually deleted
        deleted_response = client.get(url_for('user_bp.my_character_list',
                                              character_id=sample_character.id))
        assert deleted_response.status_code == 404
        assert 'message' in deleted_response.get_json()


def test_invalid_character_creation(client):
    """Test invalid character creation (missing required fields)."""
    response = client.post(url_for('user_bp.user_add_character'), json={
        'name': ''  # Missing required fields (e.g., 'name')
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Missing required fields'


def test_character_not_found(client):
    """Test fetching a non-existent character."""
    response = client.get(url_for('user_bp.my_character_list',
                                  character_id=9999))
    assert response.status_code == 404
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Character not found'
