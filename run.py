"""
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
"""

from flask import render_template
from app.models import db
from app import create_app

app = create_app()


# Home route
@app.route('/')
def index():
    return render_template('index.html')  # Ensure this template exists


@app.route('/home')
def home():
    return render_template('index.html')  # Ensure this template exists


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
