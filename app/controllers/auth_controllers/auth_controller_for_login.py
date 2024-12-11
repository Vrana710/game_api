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
