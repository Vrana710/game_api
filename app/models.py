"""=============================================================================
Project: Game Api App
Developer: Varsha Rana
File: models.py
Description: This file contains the SQLAlchemy models for the Game Api App.
             It defines the structure of the 'Users', 'House', 'Role', 'Strength',
             'Character', and 'Contact' tables in the database. The 'User' model
             handles user authentication, while the other models represent various
             aspects of the game, including character traits, roles, houses, and strengths.
             The file also includes methods for setting and verifying user passwords.
Created: 2024-12-02
Updated: 2024-12-04
=============================================================================
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(50), nullable=True)  # "Male", "Female", "Other"
    profile_picture = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        """
        Set the password for the user and update the password change timestamp.

        Parameters:
        password (str): The new password to be set. It should be a string of at least 8 characters.

        Returns:
        None
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        self.password = generate_password_hash(password)
        # Create password timestamp
        self.updated_at = datetime.now()

    def check_password(self, password):
        """
        Check if the provided password matches the hashed password stored in the User object.

        Parameters:
        password (str): The password provided by the user.

        Returns:
        bool: True if the provided password matches the hashed password, False otherwise.
        """
        return check_password_hash(self.password, password)


class House(db.Model):
    __tablename__ = 'house'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    characters = db.relationship('Character',
                                 backref='house_ref',
                                 lazy=True,
                                 cascade="none")

    def __repr__(self):
        return f"<House {self.name}>"


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    characters = db.relationship('Character',
                                 backref='role_ref',
                                 lazy=True,
                                 cascade="none")

    def __repr__(self):
        return f"<Role {self.name}>"


class Strength(db.Model):
    __tablename__ = 'strength'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    characters = db.relationship('Character',
                                 backref='strength_ref',
                                 lazy=True,
                                 cascade="none")

    def __repr__(self):
        return f"<Strength {self.name}>"


class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=True)
    animal = db.Column(db.String(100), nullable=True)
    symbol = db.Column(db.String(100), nullable=True)
    nickname = db.Column(db.String(100), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    death = db.Column(db.Integer, nullable=True)
    strength_id = db.Column(db.Integer, db.ForeignKey('strength.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp(), nullable=True)
    # Changed backref name
    house = db.relationship('House', backref='characters_in_house')
    role = db.relationship('Role', backref='characters_in_role')
    strength = db.relationship('Strength', backref='characters_in_strength')

    # Relationship with User model
    user = db.relationship('User', backref='characters_owned')

    def __repr__(self):
        return f"<Character {self.name}>"


class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
