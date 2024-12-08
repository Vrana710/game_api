# =============================================================================
# Project: Game Api App
# Developer: Varsha Rana
# File: PostgreSQLDataManager.py
# Description: This file implements the `PostgreSQLDataManager` class, which adheres
#              to the `DataManagerInterface` to perform data management operations
#              for the Game Api App. The class uses SQLAlchemy to interact with a
#              PostgreSQL database, providing a robust and flexible mechanism for
#              CRUD operations on various entities such as users, characters, houses,
#              roles, strengths, and contacts. It also includes methods to generate
#              summary reports, leveraging SQLAlchemy queries for efficient data
#              retrieval. The configuration is dynamically loaded from environment
#              variables to ensure security and adaptability across different
#              environments. This class ensures a seamless connection between
#              the application logic and database operations.
# Created: 2024-12-02
# Updated: 2024-12-08
# =============================================================================

import os
from models import db, User, House, Role, Strength, Character, Contact
from datamanager.data_manager_interface import DataManagerInterface
from dotenv import load_dotenv

load_dotenv()


class PostgreSQLDataManager(DataManagerInterface):
    """
    Data Manager class to handle database operations with PostgreSQL using SQLAlchemy.

    Attributes:
        db (SQLAlchemy): The SQLAlchemy instance to interact with the PostgreSQL database.
    """

    def __init__(self, app):
        """
        Initializes the PostgreSQLDataManager with a Flask app and configures the database.

        Args:
            app (Flask): The Flask application instance.
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        self.db = db

    # User-related methods
    def get_all_users(self):
        """Retrieve a list of all users."""
        return User.query.all()

    def add_user(self,
                 user_name,
                 user_email,
                 user_password,
                 date_of_birth=None,
                 gender=None):
        """Add a new user with optional date of birth and gender."""
        new_user = User(
            username=user_name,
            email=user_email,
            date_of_birth=date_of_birth,
            gender=gender,
            profile_picture='assets/images/default_profile.png'
        )
        new_user.set_password(user_password)
        self.db.session.add(new_user)
        self.db.session.commit()

    def update_user(self, user_id, updates):
        """Update an existing user with provided data."""
        user = User.query.get(user_id)
        if user:
            for key, value in updates.items():
                setattr(user, key, value)
            self.db.session.commit()

    def delete_user(self, user_id):
        """Delete a user based on their ID."""
        user = User.query.get(user_id)
        if user:
            self.db.session.delete(user)
            self.db.session.commit()

    def get_user_characters(self, user_id):
        """Retrieve a list of characters associated with a specific user."""
        return Character.query.filter_by(user_id=user_id).all()

    # Character-related methods
    def get_all_characters(self):
        """Retrieve a list of all characters."""
        return Character.query.all()

    def add_character(self, character_data):
        """Add a new character with the provided data."""
        new_character = Character(**character_data)
        self.db.session.add(new_character)
        self.db.session.commit()

    def update_character(self, character_id, updates):
        """Update an existing character with provided data."""
        character = Character.query.get(character_id)
        if character:
            for key, value in updates.items():
                setattr(character, key, value)
            self.db.session.commit()

    def delete_character(self, character_id):
        """Delete a character based on their ID."""
        character = Character.query.get(character_id)
        if character:
            self.db.session.delete(character)
            self.db.session.commit()

    # House-related methods
    def get_all_houses(self):
        """Retrieve a list of all houses."""
        return House.query.all()

    def add_house(self, house_name):
        """Add a new house with the provided name."""
        new_house = House(name=house_name)
        self.db.session.add(new_house)
        self.db.session.commit()

    def update_house(self, house_id, updates):
        """Update an existing house with provided data."""
        house = House.query.get(house_id)
        if house:
            for key, value in updates.items():
                setattr(house, key, value)
            self.db.session.commit()

    def delete_house(self, house_id):
        """Delete a house based on its ID."""
        house = House.query.get(house_id)
        if house:
            self.db.session.delete(house)
            self.db.session.commit()

    # Role-related methods
    def get_all_roles(self):
        """Retrieve a list of all roles."""
        return Role.query.all()

    def add_role(self, role_name):
        """Add a new role with the provided name."""
        new_role = Role(name=role_name)
        self.db.session.add(new_role)
        self.db.session.commit()

    def update_role(self, role_id, updates):
        """Update an existing role with provided data."""
        role = Role.query.get(role_id)
        if role:
            for key, value in updates.items():
                setattr(role, key, value)
            self.db.session.commit()

    def delete_role(self, role_id):
        """Delete a role based on its ID."""
        role = Role.query.get(role_id)
        if role:
            self.db.session.delete(role)
            self.db.session.commit()

    # Strength-related methods
    def get_all_strengths(self):
        """Retrieve a list of all strengths."""
        return Strength.query.all()

    def add_strength(self, strength_name):
        """Add a new strength with the provided name."""
        new_strength = Strength(name=strength_name)
        self.db.session.add(new_strength)
        self.db.session.commit()

    def update_strength(self, strength_id, updates):
        """Update an existing strength with provided data."""
        strength = Strength.query.get(strength_id)
        if strength:
            for key, value in updates.items():
                setattr(strength, key, value)
            self.db.session.commit()

    def delete_strength(self, strength_id):
        """Delete a strength based on its ID."""
        strength = Strength.query.get(strength_id)
        if strength:
            self.db.session.delete(strength)
            self.db.session.commit()

    # Contact-related methods
    def get_all_contacts(self):
        """Retrieve a list of all contacts."""
        return Contact.query.all()

    def add_contact(self, contact_name, contact_email, contact_message):
        """Add a new contact with the provided name, email, and message."""
        new_contact = Contact(name=contact_name,
                              email=contact_email,
                              message=contact_message)
        self.db.session.add(new_contact)
        self.db.session.commit()

    def delete_contact(self, contact_id):
        """Delete a contact based on its ID."""
        contact = Contact.query.get(contact_id)
        if contact:
            self.db.session.delete(contact)
            self.db.session.commit()

    # Report-related methods
    def get_reports(self):
        """Generate and retrieve reports with relevant data."""
        # Example: Replace this with your report generation logic
        return {
            "user_count": User.query.count(),
            "character_count": Character.query.count(),
            "house_count": House.query.count(),
        }
