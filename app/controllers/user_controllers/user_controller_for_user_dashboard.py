"""=============================================================================
Project: Game Api App
Developer: Varsha Rana
File: user_controller_for_user_dashboard.py
Description:
The `user_controller_for_user_dashboard.py` file is responsible for managing
the user flow related to the user dashboard in the Game API App. This controller
ensures that only authenticated users can access their dashboard, displaying
relevant user information such as profile details. The controller interacts
with the `User` model to retrieve and display the user's data. It includes
error handling for cases where the user is not logged in or does not exist.

Key Features:
1. **User Authentication**: Ensures the user is logged in before allowing access
   to the dashboard. If not, the user is redirected to the login page.
2. **User Data Fetching**: Retrieves the user's data from the database and
   ensures that the user exists before rendering the dashboard.
3. **Error Handling**: Provides error handling for cases where the user is not
   logged in or the user data cannot be found, ensuring a smooth user experience.
4. **Template Integration**: Renders the `dashboard.html` template with the
   logged-in user's data for GET requests.

Created: 2024-12-02
Updated: 2024-12-08
============================================================================="""

from flask import render_template
from app.models import User
from app.controllers.common_fun import (user_logged_in,
                                        handle_invalid_user,
                                        handle_not_logged_in)


def user_dashboard():

    if not user_logged_in():
        # Handle case where user is not logged in
        return handle_not_logged_in()

    user = user_logged_in()

    if user is None:
        return handle_invalid_user()

    # Ensure user exists or raise 404
    user = User.query.get_or_404(user.id)

    return render_template('dashboard.html',
                           user=user
                           )
