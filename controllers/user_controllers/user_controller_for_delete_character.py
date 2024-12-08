# =============================================================================
# Project: Game Api App
# Developer: Varsha Rana
# File: user_controller_for_delete_character.py
# Description:
# The `user_controller_for_delete_character.py` file is responsible for managing
# the user flow related to character deletion in the Game API App. This controller
# handles user authentication, checks if the logged-in user owns the character
# to be deleted, and processes the deletion request. It interacts with the `Character`
# model to ensure proper management of user data in the database. The file also includes
# error handling to provide feedback if an issue occurs during the deletion process.
#
# Key Features:
# 1. **User Authentication**: Verifies the user's login status before allowing
#    access to character deletion functionality.
# 2. **Character Deletion**: Checks if the character belongs to the logged-in user,
#    and if so, deletes the character from the database. If the character does not
#    belong to the user, an appropriate warning message is displayed.
# 3. **Error Handling**: Handles database errors (e.g., IntegrityError, OperationalError,
#    SQLAlchemyError) during the deletion process and provides user-friendly feedback.
# 4. **Redirect and Flash Messages**: Provides appropriate flash messages for success
#    or failure and redirects the user to the character list page after the operation.
#
# Created: 2024-12-02
# Updated: 2024-12-08
# =============================================================================


from flask import redirect, url_for, flash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, OperationalError
from models import db, Character
from controllers.common_fun import user_logged_in, handle_invalid_user, handle_not_logged_in


def delete_character(character_id):
    """
    Deletes a character from the database.
    Parameters:
    character_id (int): The ID of the character to be deleted.
    Returns:
    - If the character belongs to the current user,
      it deletes the character and redirects to the 'my_characters_list' page.
    - If the character does not belong to the current user,
      it redirects to the 'my_character_list' page with a warning message.
    - If an error occurs during the deletion process,
      it rolls back the changes and displays an error message.
    """
    if not user_logged_in():
        return handle_not_logged_in()  # Handle case where user is not logged in

    user = user_logged_in()

    if user is None:
        return handle_invalid_user()

    try:
        # Delete the character if it belongs to the current user
        deleted_rows = Character.query.filter_by(id=character_id, user_id=user.id).delete()
        if deleted_rows == 0:  # No character found for the user
            flash('Character not found or does not belong to you.', 'warning')
            return redirect(url_for('user_bp.my_character_list'))

        db.session.commit()
        flash('Character deleted successfully!', 'success')

    except IntegrityError:
        db.session.rollback()  # Rollback on integrity error
        flash('Error deleting character: Integrity error occurred.', 'danger')
    except OperationalError:
        db.session.rollback()  # Rollback on operational error
        flash('Error deleting character: A database operational error occurred.', 'danger')
    except SQLAlchemyError:
        db.session.rollback()  # Rollback on SQLAlchemy-related errors
        flash('Error deleting character: A database error occurred.', 'danger')

    return redirect(url_for('user_bp.my_character_list'))
