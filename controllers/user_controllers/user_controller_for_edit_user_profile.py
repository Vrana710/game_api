# =============================================================================
# Project: Game Api App
# Developer: Varsha Rana
# File: user_controller_for_edit_user_profile.py
# Description:
# The `user_controller_for_edit_user_profile.py` file manages the user flow
# related to editing a user's profile in the Game API App. This controller
# ensures that the logged-in user can update their profile details, including
# name, email, password, date of birth, gender, and profile picture. It validates
# the input data, handles the file upload for the profile picture, and updates
# the user's information in the database. The file also provides error handling
# for authentication and invalid user cases.
#
# Key Features:
# 1. **User Authentication**: Ensures the user is logged in before allowing access
#    to the profile edit functionality.
# 2. **Profile Data Update**: Supports updating various user profile fields, including
#    name, email, date of birth, gender, and password. It checks for changes before updating.
# 3. **Password Handling**: Only updates the password if a new password is provided,
#    ensuring the password is hashed for security.
# 4. **Profile Picture Upload**: Handles the optional upload of a profile picture,
#    validating the file type and saving the image to the server.
# 5. **Error Handling**: Provides user-friendly error handling for invalid user cases,
#    ensuring smooth user experience.
# 6. **Flash Messages**: Displays success messages upon successful profile update and
#    provides feedback to the user.
# 7. **Template Integration**: Uses the `edit_user_profile.html` template to display
#    the profile edit form for GET requests, and processes form data and updates
#    the user profile on POST requests.
#
# Created: 2024-12-02
# Updated: 2024-12-08
# =============================================================================

import os
from datetime import datetime
from flask import (render_template,
                   request,
                   redirect,
                   url_for,
                   flash,
                   current_app)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from models import db, User
from controllers.common_fun import (user_logged_in,
                                    handle_invalid_user,
                                    handle_not_logged_in,
                                    allowed_file)


def edit_user_profile(user_id):
    """
    This function handles the editing of a user's profile.
    It checks if the user is logged in,
    fetches the user's data from the database,
    validates the data, and updates the user object.
    Parameters:
    user_id (int): The ID of the user whose profile is being edited.
    Returns:
    - If the request method is POST, it returns
      a redirect to the 'user_profile' page
      if the user's profile is successfully updated.
      Otherwise, it returns the 'edit_user_profile.html'
      template with the user's information.
    - If the request method is GET, it returns
      the 'edit_user_profile.html' template
      with the user's information.
    """
    if not user_logged_in():
        return handle_not_logged_in()  # Handle case where user is not logged in

    user = user_logged_in()

    if user is None:
        return handle_invalid_user()  # Handle case where user is not valid

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        new_name = request.form.get('name', user.username)
        new_date_of_birth = request.form.get('dob', user.date_of_birth)
        new_email = request.form.get('email', user.email)
        new_gender = request.form.get('gender', user.gender)  # Optional gender field
        new_password = request.form.get('password', None)

        # Check if name has changed
        if new_name and user.username != new_name:
            user.username = new_name

        # Check if email has changed
        if new_email and user.email != new_email:
            user.email = new_email

        # Check if name has changed
        if new_date_of_birth and user.date_of_birth != new_date_of_birth:
            user.date_of_birth = new_date_of_birth

        # Update the password only if a new password was provided
        # Ensure the password is not blank
        if new_password and new_password.strip():
            user.password = generate_password_hash(new_password)
            # Optional timestamp for tracking password updates
            user.updated_at = datetime.now()

        # Check if gender has changed
        if new_gender and user.gender != new_gender:
            user.gender = new_gender

        # Handle profile picture upload (optional)
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                profile_picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(profile_picture_path)
                user.profile_picture = filename  # Save only the filename

                # Debugging: Print profile picture details
                print(f"Profile Picture Filename: {filename}")
                print(f"Profile Picture Path: {profile_picture_path}")

        db.session.commit()
        flash('Your profile updated successfully!', 'success')
        return redirect(url_for('user_bp.user_profile'))

    return render_template('edit_user_profile.html', user=user)
