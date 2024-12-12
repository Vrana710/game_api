"""=============================================================================
Project: Game API App
Developer: Varsha Rana
File: auth_controller_for_login.py
Description:
The `auth_controller_for_login.py` file defines the login functionality for
the Game API App. It handles user authentication by verifying email/username
and password credentials against the database records. The file processes login
requests and manages the user session, ensuring secure and smooth login operations.
Routes and controllers are organized to provide clear separation of concerns,
offering a modular approach to authentication.

Key Features:
1. **User Authentication**:
   - **Login**: Verifies the user's email/username and password, providing feedback on success or failure.
   - **Session Management**: Clears previous session data and stores the user's ID in the session upon successful login.

2. **Input Validation**:
   - Ensures both email and password fields are filled before processing the login attempt.

3. **Flash Messaging**:
   - Provides feedback to the user via flash messages for success or error notifications.

4. **Template Integration**:
   - Renders the `login.html` template for the login page, ensuring a seamless user interface.

Created: 2024-12-09
Updated: 2024-12-09
=============================================================================
"""
from flask import render_template, request, redirect, url_for, flash, session
from app.models import User


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
            # Redirect to the user dashboard
            return redirect(url_for('user.user_dashboard'))
        else:
            flash('Invalid email/username or password', 'danger')

    return render_template('login.html')
