# =============================================================================
# Project: Game Api App
# Developer: Varsha Rana
# File: run.py
# Description: This file initializes and configures the Flask application,
#              sets up routes for user authentication, contact form submission,
#              user registration, login/logout processes, and manages cache
#              clearing. It also includes error handling for 404 pages
#              and runs the Flask app.
# Created: 2024-12-02
# Updated: 2024-12-08
# =============================================================================
import os
import logging
from functools import cache
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from models import db, User, Contact
from blueprints.user import user_bp
from flask_caching import Cache
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
from controllers.common_fun import handle_file_upload

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)


def create_app():
    # Create the Flask app instance and configure the database URI and other settings.

    flask_app = Flask(__name__)
    # Configure the app using the Config class
    flask_app.config.from_object(Config)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['TEMPLATES_AUTO_RELOAD'] = True
    flask_app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    flask_app.config['CACHE_TYPE'] = 'simple'  # Simple in-memory cache for development
    flask_app.config['UPLOAD_FOLDER'] = './static/img/upload/profile_image'
    # Secret key for JWT encoding/decoding
    # app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")

    # Ensure the upload folder exists
    if not os.path.exists(flask_app.config['UPLOAD_FOLDER']):
        os.makedirs(flask_app.config['UPLOAD_FOLDER'])

    # Initialize the database and migration tool
    db.init_app(flask_app)
    migrate = Migrate(flask_app, db)

    # Configure and initialize cache
    cache_instance = Cache(flask_app, config={'CACHE_TYPE': 'simple'})
    cache_instance.init_app(flask_app)

    # Register Blueprints
    flask_app.register_blueprint(user_bp, url_prefix='/user')

    return flask_app


app = create_app()


# Home route
@app.route('/')
def index():
    return render_template('index.html')  # Ensure this template exists


@app.route('/home')
def home():
    return render_template('index.html')  # Ensure this template exists


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Handles the contact form submission and saves the contact details to the database.
    Renders the contact form for GET requests and processes the form data for POST requests.
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        new_contact = Contact(name=name, email=email, message=message)

        try:
            db.session.add(new_contact)
            db.session.commit()
            flash('Your message has been sent!', 'success')
            return redirect(url_for('contact'))
        except IntegrityError:
            db.session.rollback()
            flash('There was an issue saving your message. Please try again.', 'danger')

    return render_template('contact.html')


@app.route('/signup_user', methods=['GET', 'POST'])
def signup_user():
    """
    Handles the user signup process. Validates form data, hashes password, handles profile picture upload,
    creates a new User object, and saves it to the database.
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        date_of_birth = request.form['dob']
        password = request.form['password']
        gender = request.form.get('gender')  # Optional field

        if not email:
            flash('E-mail is required to create a user.', 'error')
            return redirect(url_for('signup_user'))

        if User.query.filter_by(email=email).first():
            flash('User already exists with this E-mail. Please use a different email.', 'error')
            return redirect(url_for('signup_user'))

        hashed_password = generate_password_hash(password)
        profile_picture_filename = handle_file_upload(request)

        new_user = User(
            username=username,
            email=email,
            date_of_birth=date_of_birth,
            password=hashed_password,
            gender=gender,
            profile_picture=profile_picture_filename
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            # Generate JWT token
            # token = generate_jwt_token(new_user.id)

            flash('User registration successful!', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('User with this email already exists.', 'danger')

    return render_template('singup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the login process for user.
    Verifies email/username and password against the database records.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Print the email being attempted for login
        print(f"Attempting to log in with email: {email}")

        if not password:
            flash('Both fields are required!', 'danger')
            return render_template('login.html')

        # Check if the email matches or
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):  # Verify password
            session.clear()  # Clear any previous session data
            session['user_id'] = user.id  # Store user ID in session

            flash('Login successful!', 'success')
            return redirect(url_for('user_bp.user_dashboard'))  # Redirect to the user dashboard
        else:
            flash('Invalid email/username or password', 'danger')

    return render_template('login.html')


# Clear the cache
def clear_cache():
    """
    Clears the cache if the user
    """
    # proceed to clear cache
    if hasattr(cache, 'clear'):
        cache.clear()
        flash('Cache cleared successfully!', 'success')
    else:
        flash('Cache clearing functionality not available.', 'warning')
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    """
    Handles the logout process for user.
    Clears the session data and redirects to the login page.
    """
    # if 'token' in session:
    #     session.pop('token', None)  # Remove the token from session

    if 'user_id' in session:
        clear_cache()
        session.pop('user_id', None)
        session.clear()
        return redirect(url_for('home'))
    response = make_response(redirect(url_for('login')))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    flash('You have been logged out successfully.', 'success')
    return response


# Custom error handler for 404 - Page Not Found
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Create all tables (ensure this is within an app context)
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run(debug=True)
