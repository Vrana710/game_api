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
