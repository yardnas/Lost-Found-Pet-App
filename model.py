"""Models for lost and found pets app."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin # for flask-login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

#---------------------------------------------------------------------#
# Data Model 
#     # User can have many Pets
#     # Pet can have one Location

# MVP
#     # Sign-up | Sign-in
#     # Store pet info (desc, pics, location)
#     # Show location on map (google api)

# Nice-to-have
#     # Pin location of nearest pet clinics
#     # Send an alert email | text
#     # Add chat feature
#---------------------------------------------------------------------#

class User(db.Model, UserMixin):
    """Data model for the user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(50), nullable=True)
    lname = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Foreign key between User and Pet
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'), nullable=True)


    def __repr__(self):
        """Display information about the user."""

        return f"<User user_id={self.user_id} email={self.email} fname={self.fname}>"


class Pet(db.Model):
    """Data model for the pet."""

    __tablename__ = "pets"

    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_name = db.Column(db.String(50), nullable=False)
    pet_type = db.Column(db.String(50), nullable=False)
    pet_breed = db.Column(db.String(50), nullable=False)
    pet_gender = db.Column(db.String(50), nullable=False)
    pet_color = db.Column(db.String(50), nullable=False)
    pet_image = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Foreign key between pet and location
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)

    # Add relationship between user and pets
    users = db.relationship("User", backref="pets")


    def __repr__(self):
        """Show information about the pet."""

        return f"<Pet pet_id={self.pet_id} pet_name={self.pet_name} pet_type={self.pet_type}>"


class Location(db.Model):
    """Data model for the location of the pet lost or found."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zipcode = db.Column(db.String(20), nullable=True)

    # # Foreign key between pet and location
    # pet_id = db.Column(db.Integer, db.ForeignKey('pet.pet_id'), nullable=True)

    # Add relationship between pet and location
    pet = db.relationship("Pet", backref="locations")


    def __repr__(self):
        """Show information about the location of the lost or found pet."""

        return f"<Location location_id={self.location_id} location_name={self.location_name} phone_number={self.city}"


#---------------------------------------------------------------------#

def sample_data():
    """Create sample data for testing"""

    # Empty existing data in case this is executed more than once
    User.query.delete()

    # Add sample users data
    alice = User(user_id=1, 
                pet_id=1, 
                fname="Alice",
                lname="Apple",
                phone_number="415-555-1234",
                email="alice@alice.com",
                password="alice")

    betty = User(user_id=2, 
                pet_id=2,
                fname="Bobby", 
                lname="Baker",
                phone_number="415-555-5678", 
                email="bobby@bobby.com",
                password="bobby")

    fido = Pet(pet_id=1, 
                pet_name="Fido", 
                pet_type="Dog",
                pet_breed="Corgi",
                pet_gender="Male",
                pet_color="Brown with white spots",
                pet_image="link to image",
                location_id=1)

    kitty = Pet(pet_id=2, 
                pet_name="Kitty",
                pet_type="Cat",
                pet_breed="British Shorthair",
                pet_gender="Female", 
                pet_color="Gray with black stripe tail",
                pet_image="link to image",
                location_id=2)


    fido_location = Location(location_id=1,
                            location_name="Burlingame Family Pet Hospital",
                            address="1808 Magnolia Avenue",
                            city="Burlingame",
                            state="CA",
                            zipcode="94010")

    kitty_location = Location(location_id=2,
                            location_name="Starbucks",
                            address="54 E 4th Avenue",
                            city="San Mateo",
                            state="CA",
                            zipcode="94401")

    db.session.add_all([alice, betty, fido, kitty, fido_location, kitty_location])
    db.session.commit()


def connect_to_db(flask_app):
    """Connect the database to the Flask app."""

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///lost_found_pets"
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

#---------------------------------------------------------------------#

if __name__ == "__main__":

    from server import app

    # from flask import Flask
    # app = Flask(__name__)

    # Connect to the database
    connect_to_db(app)

    # Create all tables
    db.create_all()

    # Insert sample data (adding here for now. will move to tests.py)
    sample_data()