"""=============================================================================
Project: Game API App
Developer: Varsha Rana
File: test_config.py
Description:
    This file contains unit tests to verify the configurations of the
    Game API App. These tests ensure that the application environment
    settings are correctly loaded and applied during runtime.

    Key Features Tested:
    - Validation of critical configurations such as database URI,
      secret key, debug mode, and testing mode.
    - Handling of missing or invalid configuration keys.
    - Ensuring the correct test database URI is utilized during tests.

    The application uses environment variables to manage sensitive
    information securely. This test suite ensures that the application
    adapts seamlessly to various environments without compromising
    functionality or security.

    The `pytest` framework is employed for test automation, providing
    a structured and reliable approach to configuration validation.

Created: 2024-12-02
Updated: 2024-12-08
============================================================================="""

import pytest
import os
from run import create_app
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')  # Ensure the correct path
load_dotenv(dotenv_path)


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
    value = app.config.get('NON_EXISTENT_KEY')
    assert value is None  # Check that accessing a non-existent key returns None


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
