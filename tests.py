from unittest import TestCase
from server import app
from model import connect_to_db, db, sample_data
from flask import session


class FlaskTestBasic(TestCase):
    """Flask tests basics"""

    def setup(self):
        """Things to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get('/') # making a get request
        self.assertIn(b"Lost | Found Pets", result.data) # 'b' byte string

    def test_login(self):
        """Test login page."""

        result = self.client.post('/', 
                                 data={'user_id': 'test_user1',
                                       'full_name': 'Test User1',
                                       'phone_number': '415-888-1234',
                                       'email': 'testuser@testuser.com',
                                       'password': 'test123',
                                       'user_type: 'pet_owner'},
                                        follow_redirects=True)
        
        self.assertIn(b'You ')


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Things to do before every test."""

        # Get the Flast test client
        self.client = app.test_client()

        # Display Flask errors that occurs during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        sample_data()

    def tearDown(self):
        """Things to do at the end of the test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    