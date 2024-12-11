"""=============================================================================
Project: Game API App
Developer: Varsha Rana
File: auth.py
Description:
The `auth.py` file defines the routes and controllers for authentication and
related functionalities in the Game API App. It includes user authentication
actions such as login, logout, and signup, as well as handling user contact
requests. These actions are managed under an authentication blueprint, ensuring
clean and modular route management. The file integrates various controllers
to process authentication workflows efficiently.

Key Features:
1. **User Authentication**:
   - **Login**: Provides routes for users to log in to their accounts.
   - **Logout**: Handles user logout to terminate the session securely.
   - **Signup**: Allows new users to create accounts and gain access to the app.

2. **Contact Management**:
   - Includes a route to handle user inquiries or support requests via a contact form.

3. **Blueprint Structure**:
   - Routes and controllers are organized under an `auth_bp` blueprint,
     promoting modularity and ease of maintenance.

4. **Template Integration**:
   - Templates are rendered for login, signup, and contact forms, providing
     a seamless user interface for these functionalities.

Created: 2024-12-09
Updated: 2024-12-09
============================================================================="""

import os
from flask import Blueprint

from app.controllers.auth_controllers.auth_controller_for_login import login
from app.controllers.auth_controllers.auth_controller_for_logout import logout

from app.controllers.contact_controller import contact
from app.controllers.signup_user_controller import signup_user

auth_bp = Blueprint('auth', __name__,
                    template_folder=os.path.join(os.path.dirname(__file__),
                                                 '../templates'))

auth_bp.route('/login', methods=['GET', 'POST'])(login)

auth_bp.route('/logout')(logout)

auth_bp.route('/signup_user', methods=['GET', 'POST'])(signup_user)

auth_bp.route('/contact', methods=['GET', 'POST'])(contact)
