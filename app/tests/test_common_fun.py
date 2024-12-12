"""=============================================================================
Project: Game API App
Developer: Varsha Rana
File: test_common_fun.py
Description:
The `test_common_fun.py` file contains unit tests for common utility functions
in the Game API App. Specifically, it tests the `allowed_file` function, which
determines if a given file has an acceptable extension. These tests ensure that
the file validation logic works as expected, covering different scenarios such as
valid, invalid, and edge-case file extensions.

Key Features:
1. **Testing File Validation**:
   - **Valid Extension**: Tests that files with valid extensions (e.g., `.jpg`) are accepted.
   - **Invalid Extension**: Ensures that files with unsupported extensions (e.g., `.txt`) are rejected.
   - **No Extension**: Checks the behavior when a file has no extension.
   - **Multiple Dots**: Verifies that files with multiple dots in the filename (e.g., `profile_picture.image.jpg`) are correctly handled.

2. **Unit Testing**:
   - Uses Python's `unittest` framework to execute tests and ensure correct behavior of the `allowed_file` function.

Created: 2024-12-09
Updated: 2024-12-09
=============================================================================
"""
import unittest
from app.controllers.common_fun import allowed_file


class TestCommonFun(unittest.TestCase):

    def test_allowed_file_valid_extension(self):
        filename = 'profile_picture.jpg'
        self.assertTrue(allowed_file(filename))

    def test_allowed_file_invalid_extension(self):
        filename = 'profile_picture.txt'
        self.assertFalse(allowed_file(filename))

    def test_allowed_file_no_extension(self):
        filename = 'profile_picture'
        self.assertFalse(allowed_file(filename))

    def test_allowed_file_multiple_dots(self):
        filename = 'profile_picture.image.jpg'
        self.assertTrue(allowed_file(filename))


if __name__ == '__main__':
    unittest.main()
