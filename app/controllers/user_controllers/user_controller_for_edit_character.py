"""=============================================================================
Project: Game Api App
Developer: Varsha Rana
File: user_controller_for_edit_character.py
Description:
The `user_controller_for_edit_character.py` file is responsible for managing
the user flow related to editing an existing character in the Game API App.
This controller handles user authentication, ensures that the logged-in user
has access to edit their own character, and processes the update request.
It interacts with the `Character`, `House`, `Strength`, and `Role` models
to populate the form with available data, and updates the character information
in the database after validation. Additionally, the file includes error handling
to ensure smooth user experience and security during the update process.

Key Features:
1. **User Authentication**: Verifies the user's login status before allowing
   access to the character editing page.
2. **Character Ownership Check**: Ensures that the logged-in user is the owner
   of the character they are trying to edit. If not, a warning message is shown.
3. **Dynamic Form Rendering**: Fetches available houses, roles, and strengths
   from the database to populate the character editing form.
4. **Form Handling**: Handles POST requests to update the character in the database,
   calling a function to process the update and ensuring that the submitted data is valid.
5. **Error Handling**: Gracefully handles cases where the user is not logged in,
   the user is invalid, or the character does not belong to the user, offering user-friendly feedback.
6. **Template Integration**: Utilizes the `edit_character.html` template to render
   the character editing form for GET requests and provides updated information on POST requests.

Created: 2024-12-02
Updated: 2024-12-08
============================================================================="""

from flask import render_template, request, redirect, url_for, flash
from app.models import Character, House, Strength, Role
from app.controllers.common_fun import (user_logged_in,
                                        handle_invalid_user,
                                        handle_not_logged_in,
                                        handle_character_update)


def user_edit_character(character_id):
    """
    Handles the editing of a character by a user.
    """
    if not user_logged_in():
        # Handle case where user is not logged in
        return handle_not_logged_in()

    user = user_logged_in()

    if user is None:
        # Handle case where the user is invalid
        return handle_invalid_user()

    # Fetch the character by ID and check if it belongs to the current user
    character = Character.query.get_or_404(character_id)

    if character.user_id != user.id:
        flash('You are not authorized to edit this character.', 'warning')
        # Redirect to user's characters list page
        return redirect(url_for('user_bp.my_character_list'))

    # Get related data for the form: Houses, Roles, and Strengths
    houses = House.query.all()
    roles = Role.query.all()
    strengths = Strength.query.all()

    if request.method == 'POST':
        # Call the function to handle the character update
        return handle_character_update(character)

    # For GET request, render the edit form with the current character data
    return render_template(
        'edit_character.html',
        character=character,
        user=user,
        houses=houses,
        roles=roles,
        strengths=strengths
    )
