# =============================================================================
# Project: Game Api App
# Developer: Varsha Rana
# File: user_controller_for_add_character.py
# Description:
# The `user_controller_for_add_character.py` file is responsible for managing
# the user flow related to adding a new character in the Game API App. This
# controller handles user authentication, displays the character creation form,
# and processes form submissions to create a new character. It interacts with
# the `House`, `Role`, and `Strength` models to provide dynamic options for
# character attributes. Additionally, the file includes functions to handle cases
# where the user is not logged in or provides invalid data, ensuring a secure
# and smooth user experience.
#
# Key Features:
# 1. **User Authentication**: Verifies the user's login status before allowing
#    access to the character creation page.
# 2. **Dynamic Form Rendering**: Fetches available houses, roles, and strengths
#    from the database and populates the character creation form with these options.
# 3. **Form Handling**: Processes POST requests to add new characters to the database,
#    ensuring that the submitted data is valid.
# 4. **Error Handling**: Gracefully handles cases where the user is not logged in
#    or provides invalid input, offering user-friendly feedback.
# 5. **Template Integration**: Utilizes the `add_character.html` template to
#    render the character creation form for GET requests.
#
# Created: 2024-12-02
# Updated: 2024-12-08
# =============================================================================

from flask import render_template, request
from models import House, Role, Strength
from controllers.common_fun import (
    user_logged_in,
    handle_invalid_user,
    handle_not_logged_in,
    handle_add_character_post
)


def user_add_character():
    """
    Handles the addition of a new character by a user.

    This function manages user authentication, renders the character creation form,
    and processes submitted data to add a new character. It interacts with the `House`,
    `Role`, and `Strength` models to fetch relevant options for character attributes.

    Returns:
        - Rendered HTML template for GET requests to show the form.
        - Response from `handle_add_character_post` for POST requests.
    """
    if not user_logged_in():
        return handle_not_logged_in()  # Handle case where user is not logged in

    user = user_logged_in()

    if user is None:
        return handle_invalid_user()

    if request.method == 'POST':
        return handle_add_character_post(user)

    # For GET request, prepare the list of available houses, roles, and strengths for character creation
    houses = House.query.all()
    roles = Role.query.all()
    strengths = Strength.query.all()
    return render_template(
        'add_character.html',
        houses=houses,
        roles=roles,
        strengths=strengths,
        user=user
    )
