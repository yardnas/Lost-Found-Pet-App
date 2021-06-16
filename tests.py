"""Test functions to verify code functionality."""

from unittest import TestCase
from server import app
from model import db, connect_to_db, User, Pet, sample_data


class FlaskTestsBasic(TestCase):
    """Flask basic tests."""

    def setUp(self):
        """Things to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
    

    def test_index(self):
        """Test homepage page."""

        result = self.client.get('/') 
        self.assertIn(b"Welcome", result.data) # "b" byte string


    def test_login(self):
        """Test login page"""

        # Returning from the flask test.client
        # data is a dictionary
        # result.data is the response string in the html
        result = self.client.post('login',
                                  data={'email': 'alice@alice.com', 'password': 'alice'},
                                  follow_redirects=True)
        self.assertIn(b'You have logged in succesfully', result.data)


#---------------------------------------------------------------------#

if __name__ == '__main__':
    import unittest

    connect_to_db(app)

    unittest.main()
