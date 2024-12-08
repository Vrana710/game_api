import pytest
import os
from run import create_app
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def app():
    """Create and configure the app for testing."""
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URL")
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['DEBUG'] = False
    return app


def test_configurations(app):
    """Test application configurations."""
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv("TEST_DATABASE_URL")
    assert app.config['TESTING'] is True
    assert app.config['SECRET_KEY'] == os.getenv("SECRET_KEY")
    assert app.config['DEBUG'] is False


def test_invalid_config(app):
    """Test invalid configuration handling."""
    with pytest.raises(KeyError):
        invalid_value = app.config['NON_EXISTENT_KEY']


def test_database_uri(app):
    """Test the correct database URI is used."""
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv("TEST_DATABASE_URL")


def test_debug_mode(app):
    """Test the app's debug mode."""
    assert app.config['DEBUG'] is False


def test_secret_key(app):
    """Test the secret key for sessions."""
    assert app.config['SECRET_KEY'] == os.getenv("SECRET_KEY")


def test_testing_mode(app):
    """Test the app's testing mode."""
    assert app.config['TESTING'] is True
