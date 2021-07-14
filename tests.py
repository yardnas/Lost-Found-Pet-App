"""Test functions to verify code functionality."""

#---------------------------------------------------------------------#
# TODO:
    # Test pages: index, login, logout, register, pet_reg and dashboard
    # Test database: crud functions
    # Test sessions (TODO: add sessions to code)
    # Test map & marker? (TODO: research if feasible)
#---------------------------------------------------------------------#

from unittest import TestCase
from server import app
from model import db, connect_to_db, User, Pet, test_data
import crud
import os

#---------------------------------------------------------------------#
#------------- Flask Unit Test: Render Welcome Page ------------------#
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
        self.assertIn(b"Come Join Us", result.data) # "b" byte string


#---------------------------------------------------------------------#
#-------------- Flask Unit Test: Login and Logout Tests --------------#
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
        self.assertIn(b'Please login', result.data)


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
#---------------- Flask Unit Test: TODO: Add more --------------------#
#---------------------------------------------------------------------#

# class FlaskTestDatabase(TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Things to do before every test."""

#         # Get the Flask test client
#         self.client = app.test_client()

#         # Show Flask errors that happen during tests
#         app.config['TESTING'] = True

#         # Connect to test database
#         # print("before connect to testdb")
#         connect_to_db(app, "postgresql:///testdb")
#         # print(connect_to_db)
#         # print("after connect to testdb")
#         # app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri

#         # Create tables and add sample data
#         db.create_all()
#         test_data()


#     def tearDown(self):
#         """Things to do at the end of every test."""

#         db.session.remove()
#         db.drop_all()
#         db.engine.dispose()


#     # def test_josonify_pets(self):
#     #     """Test the jsonify data for pets."""

#     #     result = self.client.get('/get/pets')
#     #     self.assertIn(b'Pitbull', result.data)

    
#---------------------------------------------------------------------#

if __name__ == '__main__':
    import unittest

    connect_to_db(app)

    unittest.main()
