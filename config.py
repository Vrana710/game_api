"""=============================================================================
Project: Game Api App
Developer: Varsha Rana
File: config.py
Description: This file contains the configuration settings for the Game Api App.
             It utilizes the `Config` class to define and manage environment-specific
             configurations such as the database connection URI, secret key for
             Flask sessions, and other Flask settings. Environment variables are
             loaded using Python's `dotenv` library to keep sensitive data secure.
             The file ensures flexibility and security by using environment variables
             while providing default fallback values where necessary. Flask testing
             mode is also enabled for development purposes.
Created: 2024-12-02
Updated: 2024-12-08
=============================================================================
"""
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Fallback to default secret key if not set
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    # Fetch DATABASE_URL from .env
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # Enable testing mode for Flask
    TESTING = True
