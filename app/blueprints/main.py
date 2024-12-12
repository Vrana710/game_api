"""=============================================================================
Project: Game API App
Developer: Varsha Rana
File: main.py
Description:
The `main.py` file defines the routes and controllers for the core functionalities
of the Game API App. It provides the main entry points for users, such as the home
page and the index route, enabling easy navigation within the app. The routes are
organized under the `main_bp` blueprint, promoting modularity and clean code organization.

Key Features:
1. **Home Page**:
   - **Index**: Displays the main landing page of the app, ensuring users are welcomed
     with an intuitive interface.
   - **Home**: Another route that renders the main content of the application,
     offering the same functionality as the index route.

2. **Blueprint Structure**:
   - Routes and controllers are organized under a `main_bp` blueprint,
     allowing for cleaner route management and separation of concerns.

3. **Template Integration**:
   - Templates for the home and index pages are rendered, offering a seamless
     user experience.

Created: 2024-12-09
Updated: 2024-12-09
============================================================================="""

from flask import render_template, Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    # Ensure this template exists
    return render_template('index.html')


@main_bp.route('/home')
def home():
    # Ensure this template exists
    return render_template('index.html')
