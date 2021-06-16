from unittest import TestCase
from server import app
from model import db, connect_to_db, User, Pet, sample_data
import os


class FlaskTestsBasic(TestCase):
    """Flask tests basics"""

    def setup(self):
        """Things to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
    

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/") 
        self.assertIn(b"Welcome", result.data) 


    # def test_login(self):
    #     """Test login page."""

    #     result = self.client.post('/', 
    #                              data={'email': 'testuser@testuser.com', 'password': 'testuser'},
    #                             follow_redirects=True)
        
    #     self.assertIn(b'You have logged in successfuly')


if __name__ == '__main__':
    import unittest

    connect_to_db(app)

    unittest.main()

    