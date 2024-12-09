"""=============================================================================
Project: Game Api App
Developer: Varsha Rana
File: data_manager_interface.py
Description: This file defines the `DataManagerInterface`, an abstract base class
             that establishes a blueprint for data management operations in the
             Game Api App. It includes abstract methods for CRUD functionality
             across various entities such as users, characters, houses, roles,
             strengths, and contacts. The interface also defines a method for
             generating and retrieving reports. By adhering to this interface,
             implementing classes ensure a consistent structure and functionality
             for handling game-related data. The interface promotes modularity
             and flexibility for future enhancements and maintenance.
Created: 2024-12-02
Updated: 2024-12-08
============================================================================="""

from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """
    An interface for data management operations, including CRUD functionality for users, characters,
    houses, roles, strengths, contacts, and generating reports.
    """

    # User-related methods
    @abstractmethod
    def get_all_users(self):
        """Retrieve a list of all users."""
        pass

    @abstractmethod
    def add_user(self,
                 user_name,
                 user_email,
                 user_password,
                 date_of_birth,
                 gender,
                 profile_picture):
        """Add a new user with optional ."""
        pass

    @abstractmethod
    def update_user(self, user_id, updates):
        """Update an existing user with provided data."""
        pass

    @abstractmethod
    def delete_user(self, user_id):
        """Delete a user based on their ID."""
        pass

    @abstractmethod
    def get_user_characters(self, user_id):
        """Retrieve a list of characters associated with a specific user."""
        pass

    # Character-related methods
    @abstractmethod
    def get_all_characters(self):
        """Retrieve a list of all characters."""
        pass

    @abstractmethod
    def add_character(self, character_data):
        """Add a new character with the provided data."""
        pass

    @abstractmethod
    def update_character(self, character_id, updates):
        """Update an existing character with provided data."""
        pass

    @abstractmethod
    def delete_character(self, character_id):
        """Delete a character based on their ID."""
        pass

    # House-related methods
    @abstractmethod
    def get_all_houses(self):
        """Retrieve a list of all houses."""
        pass

    @abstractmethod
    def add_house(self, house_name):
        """Add a new house with the provided name."""
        pass

    @abstractmethod
    def update_house(self, house_id, updates):
        """Update an existing house with provided data."""
        pass

    @abstractmethod
    def delete_house(self, house_id):
        """Delete a house based on its ID."""
        pass

    # Role-related methods
    @abstractmethod
    def get_all_roles(self):
        """Retrieve a list of all roles."""
        pass

    @abstractmethod
    def add_role(self, role_name):
        """Add a new role with the provided name."""
        pass

    @abstractmethod
    def update_role(self, role_id, updates):
        """Update an existing role with provided data."""
        pass

    @abstractmethod
    def delete_role(self, role_id):
        """Delete a role based on its ID."""
        pass

    # Strength-related methods
    @abstractmethod
    def get_all_strengths(self):
        """Retrieve a list of all strengths."""
        pass

    @abstractmethod
    def add_strength(self, strength_name):
        """Add a new strength with the provided name."""
        pass

    @abstractmethod
    def update_strength(self, strength_id, updates):
        """Update an existing strength with provided data."""
        pass

    @abstractmethod
    def delete_strength(self, strength_id):
        """Delete a strength based on its ID."""
        pass

    # Contact-related methods
    @abstractmethod
    def get_all_contacts(self):
        """Retrieve a list of all contacts."""
        pass

    @abstractmethod
    def add_contact(self, contact_name, contact_email, contact_message):
        """Add a new contact with the provided name, email, and message."""
        pass

    @abstractmethod
    def delete_contact(self, contact_id):
        """Delete a contact based on its ID."""
        pass

    # Report-related methods
    @abstractmethod
    def get_reports(self):
        """Generate and retrieve reports with relevant data."""
        pass
