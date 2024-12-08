# =============================================================================
# Project: Game Api App
# Developer: Varsha Rana
# File: user_controller_for_view_user_profile.py
# Description:
# The `user_controller_for_view_user_profile.py` file handles the user flow
# related to displaying and managing the user profile in the Game API App.
# This controller ensures that the logged-in user can view their profile
# details, including information stored in the database. It checks whether
# the user is logged in, fetches the user’s data, and displays the profile
# using the `view_user_profile.html` template. If the user is not logged in
# or the user data is invalid, appropriate redirection or error handling is performed.
#
# Key Features:
# 1. **User Authentication**: Verifies that the user is logged in before
#    granting access to their profile. If not, redirects to the login page.
# 2. **User Data Fetching**: Retrieves the logged-in user's data from the database
#    and ensures that the profile page displays correct information.
# 3. **Error Handling**: Provides error handling for invalid users and redirects
#    them accordingly.
# 4. **Template Integration**: Renders the `view_user_profile.html` template
#    to display the user's profile information.
# 5. **Redirect Handling**: Redirects to the login page or an error page if the user
#    is not logged in or if their user data is invalid.
#
# Created: 2024-12-02
# Updated: 2024-12-08
# =============================================================================


from flask import render_template
from models import User
from controllers.common_fun import (user_logged_in,
                                    handle_invalid_user,
                                    handle_not_logged_in
                                    )


def user_profile():
    """
    This function handles the user profile page.
    It checks if the user is logged in,
    fetches the user's data from the database,
    and renders the 'user_profile.html'
    template with the user's information.
    Parameters:
    None
    Returns:
    - If the user is logged in, it returns the 'user_profile.html' template
      with the user's information.
    - If the user is not logged in, it redirects to the 'login' page.
    """
    if not user_logged_in():
        return handle_not_logged_in()  # Handle case where user is not logged in

    user = user_logged_in()

    if user is None:
        return handle_invalid_user()  # Handle case where user is not valid

    user_id = User.query.get(user.id)

    return render_template('view_user_profile.html', user=user_id)
