import os
import unittest
from unittest.mock import MagicMock
from app import create_app
from app.controllers.common_fun import handle_file_upload
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class TestFileUpload(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        # Initialize the app using the create_app function
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URL")
        self.app.config['SERVER_NAME'] = 'localhost:5000'  # or your domain/host
        self.app.config['APPLICATION_ROOT'] = '/'  # The root path of your application
        # Ensure the app is in test mode
        self.app.config['TESTING'] = True
        self.app.config['UPLOAD_FOLDER'] = './app/static/img/upload/profile_image'

        # Mock the folder existence in case it's not created during the test
        if not os.path.exists(self.app.config['UPLOAD_FOLDER']):
            os.makedirs(self.app.config['UPLOAD_FOLDER'])

    def test_handle_file_upload_success(self):
        """Test the file upload with a valid image."""
        # Mocking the file upload
        mock_upload_request = MagicMock()
        mock_upload_request.files = {'profile_picture': MagicMock(filename='profile_picture.jpg')}
        mock_upload_request.files['profile_picture'].save = MagicMock()

        # Push the application context to make 'current_app' accessible
        with self.app.app_context():
            filename = handle_file_upload(mock_upload_request)

        # Check that the returned filename matches the expected file
        self.assertEqual(filename, 'profile_picture.jpg')

        # Check that the save method was called once
        mock_upload_request.files['profile_picture'].save.assert_called_once()

    def test_handle_file_upload_no_file(self):
        """Test the file upload with no file uploaded."""
        # Mocking an empty upload
        mock_upload_request = MagicMock()
        mock_upload_request.files = {}

        # Push the application context to make 'current_app' accessible
        with self.app.app_context():
            filename = handle_file_upload(mock_upload_request)

        # Check that no file was uploaded and None is returned
        self.assertIsNone(filename)

    def test_handle_file_upload_invalid_extension(self):
        """Test the file upload with an invalid file extension."""
        # Mocking an invalid file upload (non-image file)
        mock_upload_request = MagicMock()
        mock_upload_request.files = {'profile_picture': MagicMock(filename='profile_picture.txt')}

        # Push the application context to make 'current_app' accessible
        with self.app.app_context():
            filename = handle_file_upload(mock_upload_request)

        # Check that the file with an invalid extension returns None
        self.assertIsNone(filename)

    def tearDown(self):
        """Clean up any files or resources after tests."""
        # Optionally clean up the upload folder after tests if needed
        pass

    if __name__ == '__main__':
        unittest.main()
