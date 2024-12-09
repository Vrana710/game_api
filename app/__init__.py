"""
=============================================================================
Project: Game API App
Developer: Varsha Rana
File: __init__.py
Description: Initializes the Game API application and configures its core
             components. The app uses Flask with SQLAlchemy for PostgreSQL
             database interactions, supporting CRUD operations for entities
             like users, contacts, and more. It includes caching and migration
             tools for optimized performance and adaptability. The configuration
             is securely managed via environment variables, ensuring flexible
             deployment across environments.
Created: 2024-12-02
Updated: 2024-12-08
=============================================================================
"""

import os
import logging
from flask import Flask
from app.models import db, User, Contact
from app.blueprints.user import user_bp
from flask_caching import Cache
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
from app.controllers.common_fun import handle_file_upload

# Set up logging
logging.basicConfig(level=logging.DEBUG)
load_dotenv()

migrate = Migrate()
cache_instance = Cache()


def create_app():
    app = Flask(__name__)

    # Configure the app using the Config class
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['CACHE_TYPE'] = 'simple'  # Simple in-memory cache for development
    app.config['UPLOAD_FOLDER'] = './app/static/img/upload/profile_image'

    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Initialize the database and migration tool
    db.init_app(app)
    migrate.init_app(app, db)

    # Configure and initialize cache
    # cache_instance = Cache(app, config={'CACHE_TYPE': 'simple'})
    cache_instance.init_app(app)

    # Register Blueprints
    from .blueprints.user import user_bp
    from .blueprints.auth import auth_bp

    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
