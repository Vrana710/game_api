"""=============================================================================
Project: Game API App
Developer: Varsha Rana
File: signup_user_controller.py
Description:
The `signup_user_controller.py` file defines the logic for managing user
registration in the Game API App. It handles the user signup process, including
validating input, hashing passwords, managing profile picture uploads, and saving
new user data to the database. This file ensures a secure and seamless signup
experience for new users.

Key Features:
1. **User Signup Process**:
   - **Form Validation**: Ensures required fields are filled and verifies
     that the email is unique.
   - **Password Hashing**: Secures user passwords by storing them in a hashed format.

2. **Profile Picture Upload**:
   - Handles optional profile picture uploads, ensuring that files are stored
     securely and linked to the user profile.

3. **Database Integration**:
   - Creates and stores new user records in the database with all relevant details.

4. **Error Handling**:
   - Provides meaningful error messages for validation failures or database
     conflicts, such as duplicate email addresses.

5. **User Feedback**:
   - Displays success or error messages to inform users about the status
     of their registration.

6. **Template Integration**:
   - Renders the `signup.html` template, offering a user-friendly interface
     for the signup process.

7. **Security**:
   - Implements secure password storage and provides scope for JWT token
     generation for user authentication.

Created: 2024-12-02
Updated: 2024-12-08
============================================================================="""

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from flask import flash, redirect, render_template, request, url_for
from app.models import User, db
from app.controllers.common_fun import handle_file_upload


def signup_user():
    """
    Handles the user signup process. Validates form data, hashes password,
    handles profile picture upload,
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
            return redirect(url_for('auth.signup_user'))

        if User.query.filter_by(email=email).first():
            flash('User already exists with this E-mail. Please use a different email.', 'error')
            return redirect(url_for('auth.signup_user'))

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

            flash('User registration successful!', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('User with this email already exists.', 'danger')

    return render_template('singup.html')
