"""Test functions to verify code functionality."""

#---------------------------------------------------------------------#
# Test pages: index, login, logout, register, pet_register and dashboard
# Test database: crud functions
# Test sessions (TODO: add sessions to code)
# Test map & marker? (TODO: research if feasible)
#---------------------------------------------------------------------#

from unittest import TestCase
from server import app
from model import db, connect_to_db, User, Pet, sample_data

#---------------------------------------------------------------------#
#---------------------- Unit Test: Basic Tests -----------------------#
#---------------------------------------------------------------------#

class FlaskTestsBasic(TestCase):
    """Flask basic test."""

    def setUp(self):
        """Things to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
    

    def test_index(self):
        """Test welcome page."""

        result = self.client.get('/') 
        self.assertIn(b"Welcome", result.data) # "b" byte string

#---------------------------------------------------------------------#
#---------------- Unit Test: Login and Logout Tests ------------------#
#---------------------------------------------------------------------#

class FlaskTestsLogInLogOut(TestCase):
    """Flask tests of user login and logout."""

    def setUp(self):
        """Things to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True


    def test_login_page(self):
        """Test that the login page loads properly."""

        result = self.client.get('/login')
        self.assertIn(b'Please sign in', result.data)


    def test_correct_login(self):
        """Test login when credentials are correct."""


        result = self.client.post('/login',
                                  data={'email': 'alice@alice.com', 'password': 'alice'},
                                  follow_redirects=True)
        self.assertIn(b'You have logged in succesfully', result.data) 

    
    def test_incorrect_login(self):
        """Test login when credentials are incorrect."""

        result = self.client.post('/login',
                                  data={'email': 'not@valid.com', 'password': 'notvalid'},
                                  follow_redirects=True)
        self.assertIn(b'Please try again', result.data)


    def test_logout(self):
        """Test logout page"""

        self.client.post('/login',
                         data={'email': 'alice@alice.com', 'password': 'alice'},
                         follow_redirects=True
        )

        result = self.client.get('/logout',
                                 follow_redirects=True)
        self.assertIn(b'Logged out successfully', result.data)

    
#---------------------------------------------------------------------#

if __name__ == '__main__':
    import unittest

    connect_to_db(app)

    unittest.main()
