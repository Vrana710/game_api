"""=============================================================================
Project: Game API App
Developer: Varsha Rana
File: contact_controller.py
Description:
The `contact_controller.py` file defines the logic for handling user contact
requests in the Game API App. It includes a controller function to manage the
contact form, allowing users to submit inquiries or feedback. This file ensures
that user-submitted data is processed and stored in the database securely, while
also providing feedback to the user about the status of their submission.

Key Features:
1. **Contact Form Management**:
   - **GET Requests**: Renders the contact form template for users to fill out.
   - **POST Requests**: Processes submitted form data and saves it to the database.

2. **Database Integration**:
   - Captures and stores contact details such as name, email, and message
     using the database.

3. **Error Handling**:
   - Implements error handling for database operations, ensuring robust data
     management and providing meaningful feedback in case of issues.

4. **User Feedback**:
   - Provides success or error messages to inform users about the status
     of their message submission.

5. **Template Integration**:
   - Renders the `contact.html` template to provide a user-friendly interface
     for submitting inquiries or feedback.

Created: 2024-12-02
Updated: 2024-12-08
============================================================================="""
from sqlalchemy.exc import IntegrityError
from flask import request, render_template, flash, redirect, url_for
from app.models import db, Contact


def contact():
    """
    Handles the contact form submission and saves the contact details to the database.
    Renders the contact form for GET requests and processes the form data for POST requests.
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        new_contact = Contact(name=name, email=email, message=message)

        try:
            db.session.add(new_contact)
            db.session.commit()
            flash('Your message has been sent!', 'success')
            return redirect(url_for('auth_bp.contact'))
        except IntegrityError:
            db.session.rollback()
            flash('There was an issue saving your message. Please try again.', 'danger')

    return render_template('contact.html')
