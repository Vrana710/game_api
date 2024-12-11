"""=============================================================================
Project: Game Api App
Developer: Varsha Rana
File: user.py
Description:
The `user.py` file defines the routes and controllers for user-related
functionalities in the Game API App. It includes various user-specific
actions, such as viewing and editing the user profile, managing character
data (viewing, adding, editing, and deleting characters), and accessing the
user dashboard. The file integrates different controllers to handle these
actions, and organizes them under a user blueprint for clean route management.
Each route is mapped to its respective controller function, ensuring that
users can easily interact with the app’s features through a well-structured API.

Key Features:
1. **User Dashboard**: Provides access to the user's dashboard where they
   can view an overview of their activities, including character data and profile.
2. **Character Management**: Allows users to view their characters, add new
   characters, edit existing ones, and delete characters as needed.
3. **User Profile**: Users can view and edit their profile details. It includes
   routes for displaying and updating personal information.
4. **Blueprint Structure**: Routes and controllers are organized under a
   `Blueprint` for user-related functionalities, making the app modular and easy
   to maintain.
5. **Template Integration**: The routes render templates to display character
   lists, user profiles, and forms for adding/editing characters and profiles.

Created: 2024-12-02
Updated: 2024-12-08
============================================================================="""


import os
from flask import Blueprint

from app.controllers.user_controllers.user_controller_for_user_dashboard \
    import user_dashboard

from app.controllers.user_controllers.user_controller_for_view_character_list \
    import my_character_list
from app.controllers.user_controllers.user_controller_for_add_character \
    import user_add_character
from app.controllers.user_controllers.user_controller_for_delete_character \
    import delete_character
from app.controllers.user_controllers.user_controller_for_edit_character \
    import user_edit_character

from app.controllers.user_controllers.user_controller_for_view_user_profile \
    import user_profile
from app.controllers.user_controllers.user_controller_for_edit_user_profile \
    import edit_user_profile

user_bp = Blueprint('user', __name__,
                    template_folder=os.path.join(os.path.dirname(__file__),
                                                 '../templates/user'))


user_bp.route('/dashboard')(user_dashboard)

user_bp.route('/character_list', methods=['GET'])(my_character_list)
user_bp.route('/add_character', methods=['GET', 'POST'])(user_add_character)
user_bp.route('/edit_character/<int:character_id>',
              methods=['GET', 'POST'])(user_edit_character)
user_bp.route('/delete_character/<int:character_id>',
              methods=['POST'])(delete_character)

user_bp.route('/user_profile')(user_profile)
user_bp.route('/edit_user_profile/<int:user_id>',
              methods=['GET', 'POST'])(edit_user_profile)
