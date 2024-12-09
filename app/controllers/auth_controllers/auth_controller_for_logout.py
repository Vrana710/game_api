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
        return redirect(url_for('auth_bp.login'))

    response = make_response(redirect(url_for('auth_bp.login')))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    flash('You have been logged out successfully.', 'success')
    return response
