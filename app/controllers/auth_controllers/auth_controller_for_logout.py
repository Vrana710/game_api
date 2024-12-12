"""=============================================================================
Project: Game API App
Developer: Varsha Rana
File: auth_controller_for_logout.py
Description:
The `auth_controller_for_logout.py` file defines the logout functionality for
the Game API App. It handles the process of logging users out by clearing session
data, including user-specific identifiers, and redirecting them to the login page.
The file ensures secure and clean session termination, preventing unauthorized access
after logout. Flash messages are provided to inform users of the successful logout process.

Key Features:
1. **User Logout**:
   - **Session Clearing**: Clears user-specific session data (e.g., user ID) to securely log out the user.
   - **Cache Control**: Prevents the browser from caching sensitive session information after logout.

2. **Redirect**:
   - Redirects the user to the login page after logout to ensure they cannot access restricted areas without logging back in.

3. **Flash Messaging**:
   - Provides feedback to the user via a success message, indicating that the logout was successful.

4. **Template and Response Management**:
   - Ensures proper HTTP headers (e.g., Cache-Control, Pragma, Expires) are set to prevent caching of sensitive data.

Created: 2024-12-09
Updated: 2024-12-09
=============================================================================
"""
from flask import redirect, url_for, flash, session, make_response
from app.controllers.common_fun import clear_cache


def logout():
    """
    Handles the logout process for user.
    Clears the session data and redirects to the login page.
    """
    # if 'token' in session:
    #     session.pop('token', None)  # Remove the token from session

    if 'user_id' in session:
        clear_cache()
        session.pop('user_id', None)
        session.clear()
        return redirect(url_for('auth.login'))

    response = make_response(redirect(url_for('auth_bp.login')))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    flash('You have been logged out successfully.', 'success')
    return response
