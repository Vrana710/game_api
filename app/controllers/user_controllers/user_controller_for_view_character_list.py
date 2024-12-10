"""=============================================================================
Project: Game Api App
Developer: Varsha Rana
File: user_controller_for_view_character_list.py
Description:
The `user_controller_for_view_character_list.py` file handles the user flow
related to displaying and managing the list of characters in the Game API App.
This controller retrieves and displays a list of characters associated with
the logged-in user. It supports search, filtering, sorting, and pagination,
allowing the user to easily navigate and manage their characters. The file
applies various filters based on the user's input, such as house, role, strength,
and age. It also handles sorting by character attributes and supports AJAX
requests for partial page updates, improving user experience.

Key Features:
1. **User Authentication**: Ensures that the user is logged in before
   allowing access to the character list. If not, redirects to the login page.
2. **Character Data Fetching**: Retrieves the list of characters related
   to the logged-in user, and supports dynamic filtering based on search
   queries and multiple filters (e.g., house, role, strength, age).
3. **Search Functionality**: Supports searching characters by name using
   a case-insensitive search query.
4. **Filter Options**: Allows users to filter characters by house, role,
   strength, and age using dropdowns or range inputs.
5. **Sorting Functionality**: Users can sort characters by various columns
   (e.g., name, age) in ascending or descending order.
6. **Pagination**: Implements pagination for the character list, with
   a fixed number of characters displayed per page.
7. **AJAX Support**: Handles AJAX requests for partial page updates, enabling
   smoother user interactions without reloading the entire page.
8. **Template Integration**: Renders the `character_list.html` template for
   displaying the full character list and the `partials/manage_character_content.html`
   template for AJAX responses.

Created: 2024-12-02
Updated: 2024-12-08
============================================================================="""

from flask import render_template, request
from app.models import Character, House, Role, Strength
from app.controllers.common_fun import (user_logged_in,
                                        handle_invalid_user,
                                        handle_not_logged_in)


def my_character_list():
    """
    Handles character list
    """
    if not user_logged_in():
        # Handle case where user is not logged in
        return handle_not_logged_in()

    user = user_logged_in()
    if user is None:
        # Handle case where the user object is invalid
        return handle_invalid_user()

    # Fetch filter and sorting parameters
    filters = {
        "search_query": request.args.get('search', '', type=str).lower(),
        "house_filter": request.args.get('house', '', type=str),
        "role_filter": request.args.get('role', '', type=str),
        "strength_filter": request.args.get('strength', '', type=str),
        "age_more_than": request.args.get('age_more_than', '', type=int),
        "age_less_than": request.args.get('age_less_than', '', type=int),
    }
    sort_options = {
        "sort_column": request.args.get('sort_column', 'name'),
        "sort_order": request.args.get('sort_order', 'asc'),
    }
    pagination = {
        "page": request.args.get('page', 1, type=int),
        "per_page": 5,
    }

    # Build query
    query = build_character_query(user.id, filters, sort_options)

    # Pagination logic
    num_characters = query.count()
    characters_query = query.paginate(page=pagination["page"], per_page=pagination["per_page"])

    # Determine if the request is AJAX for partial rendering
    template = (
        'partials/manage_character_content.html'
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        else 'character_list.html'
    )

    return render_template(
        template,
        user=user,
        num_characters=num_characters,
        characters_query=characters_query,
        **filters,
        **sort_options
    )


def build_character_query(user_id, filters, sort_options):
    """
    Builds the character query with filters and sorting.
    """
    query = Character.query.filter_by(user_id=user_id)

    # Apply filters
    if filters["search_query"]:
        query = query.filter(Character.name.ilike(f"%{filters['search_query']}%"))
    if filters["house_filter"]:
        query = query.filter(Character.house.has(House.name.ilike(f"%{filters['house_filter']}%")))
    if filters["role_filter"]:
        query = query.filter(Character.role.has(Role.name.ilike(f"%{filters["role_filter"]}%")))
    if filters["strength_filter"]:
        query = query.filter(Character.strength.has(Strength.name.ilike(f"%{filters["strength_filter"]}%")))
    if filters["age_more_than"]:
        query = query.filter(Character.age >= filters["age_more_than"])
    if filters["age_less_than"]:
        query = query.filter(Character.age <= filters["age_less_than"])

    # Apply sorting
    sort_column = sort_options["sort_column"]
    sort_order = sort_options["sort_order"]
    if sort_order == 'asc':
        query = query.order_by(getattr(Character, sort_column).asc())
    else:
        query = query.order_by(getattr(Character, sort_column).desc())

    return query
