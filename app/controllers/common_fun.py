"""=============================================================================
Project: Game API App
Developer: Varsha Rana
File: common_fun.py
Description:
The `common_fun.py` file serves as a utility module for the Game API App,
implementing essential functions and methods to streamline data handling
and user interactions. It encompasses a wide range of functionalities such as:
managing file uploads, user session handling, database interactions,
and CRUD operations for key entities like characters, houses, roles, strengths,
and users. These utilities aim to reduce redundancy, enhance maintainability,
and provide a consistent user experience throughout the application.

Key Features:
1. File Uploads:
   - Validates file types and securely handles image uploads for profile pictures.

2. User Session Management:
   - Verifies user login status and ensures smooth handling of invalid or expired sessions.

3. Character Management:
   - Offers functions to create, update, and manage character data, including
     associated entities like houses, roles, and strengths.

4. Database Interaction:
   - Employs SQLAlchemy ORM for efficient and reliable database transactions,
     with rollback mechanisms to preserve data integrity.

5. Error Handling:
   - Provides robust error handling with detailed feedback using flash messages,
     improving usability and user guidance.

6. Cache Management:
   - Includes utilities to clear application cache, ensuring optimal performance.

Created: 2024-12-02
Updated: 2024-12-08
=============================================================================
"""
import os
from flask import (
    request,
    redirect,
    url_for,
    session,
    flash,
    current_app,
    make_response)
from werkzeug.utils import secure_filename
from app.models import db, User, Character, Role, Strength, House
from app.blueprints.utils import fetch_character_data

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """
    Check if a filename has a valid extension.
    Parameters:
    filename (str): The name of the file to check.
    Returns:
    bool: True if the filename has a valid extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_file_upload(upload_request):
    """
       Handles the file upload for a profile picture.

       This function checks if the uploaded request contains a file named 'profile_picture'.
       If the file is found and has an allowed extension, it is saved to the specified
       upload folder with a secure filename. The function then returns the filename of
       the saved profile picture. If the file is not found or not allowed, it returns None.

       Parameters:
       upload_request (werkzeug.datastructures.FileStorage): The file upload request.

       Returns:
       str or None: The filename of the uploaded profile picture if successful, None otherwise.
       """
    if 'profile_picture' in upload_request.files:
        file = upload_request.files['profile_picture']
        if file and allowed_file(file.filename):
            profile_picture_filename = secure_filename(file.filename)
            profile_picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                                profile_picture_filename)
            file.save(profile_picture_path)
            return profile_picture_filename
    return None


def user_logged_in():
    """Check if the user is logged in."""
    user_id = session.get('user_id')
    if user_id:
        # This should return the User object or None
        return User.query.get(user_id)
    return None


def handle_not_logged_in():
    """Handle case where admin is not logged in."""
    if 'user_id' in session:
        clear_cache()
        session.pop('user_id', None)
        session.clear()
    return redirect(url_for('auth.login'))


def clear_cache():
    """Clear cache if it exists."""
    cache = current_app.extensions.get('cache')
    if cache and hasattr(cache, 'clear'):
        cache.clear()

    response = make_response(redirect(url_for('auth.login')))
    response.headers['Cache-Control'] = ('no-store, '
                                         'no-cache, '
                                         'must-revalidate, '
                                         'post-check=0, '
                                         'pre-check=0, '
                                         'max-age=0')
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


def handle_invalid_user():
    """Handle the case where the user is not valid."""
    session.clear()
    clear_cache()
    flash('Invalid user. Please log in again.',
          'error')
    # Redirect to login page
    return redirect(url_for('auth.login'))


def handle_missing_character_name():
    """Handle the case where the missing character_name."""
    flash('Character name is required!', 'danger')
    return redirect(url_for('user.user_add_character'))


def handle_invalid_character_data():
    """
    Handles the case where the fetched character data is
    invalid or incomplete.
    """
    flash('Invalid character data received. '
          'Please check the data source or try again later.',
          'danger')
    return redirect(url_for('user.my_character_list'))


def handle_missing_character_data():
    """
    Handles the case where character data could not be retrieved or is missing.
    """
    flash('Character data could not be found. '
          'Please check the character name and try again.', 'danger')
    return redirect(url_for('user.user_add_character'))


def handle_add_character_post(user):
    """Handle POST request for adding a character."""
    user_id = session['user_id']
    character_name = request.form.get('name')

    # Check if character name is provided
    if not character_name:
        return handle_missing_character_name()

    # Check if the character already exists
    if check_existing_character(character_name, user_id):
        flash('Character with this name already exists.', 'warning')
        return redirect(url_for('user.my_character_list'))

    # Fetch character data (from JSON or another source)
    character_data = fetch_character_data(character_name)
    print("DEBUG :", character_data)
    if not character_data:
        return handle_missing_character_data()

    # Create a new character using the fetched data
    new_character = create_character_from_data(character_data, user)
    if not new_character:
        return handle_invalid_character_data()

    # Save the new character to the database
    return save_new_character(new_character)


def check_existing_character(character_name, user_id):
    """
    Checks if a character with the given name already
    exists for the specified admin.
    """
    character = Character.query.filter_by(name=character_name,
                                          user_id=user_id).first()
    return character is not None


def create_character_from_data(character_data, user):
    """
    Creates a new character from the fetched character data.

    Parameters:
    - character_data (dict): The data used to create the character.
    - user (User): The user associated with this character.

    Returns:
    - Character: A new Character object or None if the data is invalid.
    """
    # Fetch and validate character data
    character_name = character_data.get('name')
    house_name = character_data.get('house')
    role_name = character_data.get('role')
    strength_name = character_data.get('strength')

    if not character_name:
        print("Character name is missing.")
        return None

    # Find or create associated models
    house = find_or_create_house(house_name) if house_name else None
    role = find_or_create_role(role_name) if role_name else None
    strength = find_or_create_strength(strength_name) if strength_name else None

    try:
        new_character = Character(
            name=character_name,
            house=house,
            animal=character_data.get('animal'),
            symbol=character_data.get('symbol'),
            nickname=character_data.get('nickname'),
            role=role,
            age=character_data.get('age'),
            death=character_data.get('death'),
            strength=strength,
            user_id=user.id
        )
        return new_character
    except KeyError as e:
        print(f"Missing key in character data: {e}")
        return None


def find_or_create_house(house_name):
    """
    Finds or creates a House based on the given name.
    """
    house = House.query.filter_by(name=house_name).first()
    if not house:
        house = House(name=house_name)
        db.session.add(house)
        db.session.commit()
    return house


def find_or_create_role(role_name):
    """
    Finds or creates a Role based on the given name.
    """
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        role = Role(name=role_name)
        db.session.add(role)
        db.session.commit()
    return role


def find_or_create_strength(strength_name):
    """
    Finds or creates a Strength based on the given name.
    """
    strength = Strength.query.filter_by(name=strength_name).first()
    if not strength:
        strength = Strength(name=strength_name)
        db.session.add(strength)
        db.session.commit()
    return strength


def save_new_character(character):
    """
    Saves the new character to the database and commits the transaction.
    """
    try:
        db.session.add(character)
        db.session.commit()
        flash('Character added successfully!',
              'success')
        return redirect(url_for('user.my_character_list'))
    except Exception as e:
        db.session.rollback()
        print(f"Error saving character: {e}")
        flash('Error adding character: Database error occurred.',
              'danger')
        return redirect(url_for('user.user_add_character'))


def handle_character_update(character):
    """
    Handles the update of a character's details.
    """
    try:
        # Get updated data from the form
        updated_data = {
            'name': request.form.get('name'),
            'house_id': request.form.get('house_id'),
            'animal': request.form.get('animal'),
            'symbol': request.form.get('symbol'),
            'nickname': request.form.get('nickname'),
            'role_id': request.form.get('role_id'),
            'age': request.form.get('age'),
            'death': request.form.get('death'),
            'strength_id': request.form.get('strength_id')
        }

        # Ensure the form data is not empty or invalid
        if not updated_data['name']:
            flash('Character name is required.',
                  'danger')
            return redirect(url_for('user.edit_character',
                                    character_id=character.id))

        # Handle 'death' field (convert empty string to None for NULL in the database)
        if updated_data['death'] == '':
            updated_data['death'] = None

        # Update the character's details with the new data
        for key, value in updated_data.items():
            # Convert age and death to integers if present
            if key in ['age'] and value:
                value = int(value)
            setattr(character, key, value)

        # Commit changes to the database
        db.session.commit()

        flash('Character updated successfully!',
              'success')
        # Redirect to the character list page
        return redirect(url_for('user.my_character_list'))

    except Exception as e:
        # Rollback the session if an error occurs
        db.session.rollback()
        flash(f'Error updating character: {str(e)}',
              'danger')
        # Redirect to the user's characters list page
        return redirect(url_for('user.my_character_list'))
