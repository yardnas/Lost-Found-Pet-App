"""Models for lost and found pets app."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin # for flask-login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

#---------------------------------------------------------------------#
#-------------------------- MVP Scope Section ------------------------#
#---------------------------------------------------------------------#
# Data Model 
    # User can have many Pets
    # Pet can have one owner
    # Instead of Location, added address to Pet

# MVP
    # Sign-up | Sign-in | Log-out => used flask-login to achieve
    # Store pet info (desc, pics, location) => stored in postgres db
    # Show pet info & location on the map => utilize the google maps api

# My MVP update on Mon, 6/14/21 (End of Sprint 1)
    # I was behind and was catching up on lectures ==> hit MVP late yesterday (Sunday)
    # My MVP (list above)
    # Today: will work on password hash and test.py to find bugs I'm sure I have => I may join the group chat with Maura
    # Next feature if have time: dynamically pin location by entering "location" (golden gate bridge) opposed to entering the address
    # Not block at the moment

# Nice-to-have
    # Dynamically pin location by entering location (opposed to filling out the registration page)
        # - need to save pin/marker address from geocode form 
        # - need to get real address from geocode input
        # - need to store address in db
        # - need to add pet info & address/location on map

     # Add test and seed
     # Add nearby places: vet clinics, police station
     # Send an alert email | text
     # Add chat feature


#---------------------------------------------------------------------#
#------------------------- Data Model Section ------------------------#
#---------------------------------------------------------------------#

class User(db.Model, UserMixin):
    """Data model for the user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    fname = db.Column(db.String(50), nullable=True)
    lname = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


    # To address error: NotImplementedError: No 'id' attribute - override 'get_id'
    def get_id(self):
           return (self.user_id)
    

    def __repr__(self):
        """Display information about the user."""

        return f"<User user_id={self.user_id} email={self.email} fname={self.fname}>"


class Pet(db.Model):
    """Data model for the pet."""

    __tablename__ = "pets"

    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    pet_name = db.Column(db.String(50), nullable=False)
    pet_type = db.Column(db.String(50), nullable=False)
    pet_breed = db.Column(db.String(50), nullable=False)
    pet_gender = db.Column(db.String(50), nullable=False)
    pet_color = db.Column(db.String(50), nullable=False)
    pet_image = db.Column(db.String(50), nullable=True)
    last_address = db.Column(db.String(100), nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Add relationship between users and pets
    users = db.relationship("User", backref="pet")

    def __repr__(self):
        """Show information about the pet."""

        return f"<Pet pet_id={self.pet_id} pet_name={self.pet_name} pet_type={self.pet_type}>"


class Location(db.Model):
    """Data model for the location of the pet lost or found."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'))

    location_name = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zipcode = db.Column(db.String(20), nullable=True)

    # # # Add relationship between pets and locations
    pets = db.relationship("Pet", backref="location")


    def __repr__(self):
        """Show information about the location of the lost or found pet."""

        return f"<Location location_id={self.location_id} location_name={self.location_name} phone_number={self.city}"


#---------------------------------------------------------------------#
#------------------------ Sample Data Section ------------------------#
#---------------------------------------------------------------------#

def sample_data():
    """Create sample data for testing"""

    # Empty existing data in case this is executed more than once
    User.query.delete()

    # Add sample users data
    alice = User(user_id=101, 
                fname="Alice",
                lname="Apple",
                phone="415-555-1234",
                email="alice@alice.com",
                password="alice")

    betty = User(user_id=102, 
                fname="Bobby", 
                lname="Baker",
                phone="415-555-5678", 
                email="bobby@bobby.com",
                password="bobby")

    fido = Pet(pet_id=101, 
                user_id=101,
                pet_name="Fido", 
                pet_type="Dog",
                pet_breed="Bulldog",
                pet_gender="Male",
                pet_color="White with blk spots on ears",
                pet_image="/static/img/dog_bulldog.jpg",
                last_address="54 E 4th Ave, San Mateo, CA 94401")

    kitty = Pet(pet_id=102,
                user_id=102,
                pet_name="Kitty",
                pet_type="Cat",
                pet_breed="British Shorthair",
                pet_gender="Female", 
                pet_color="Grey with orange eyes",
                pet_image="/static/img/cat_grey.jpg",
                last_address="1230 Broadway, Burlingame, CA 94010")


    fido_location = Location(location_id=101,
                            pet_id=101,
                            location_name="Burlingame Family Pet Hospital",
                            address="1808 Magnolia Avenue",
                            city="Burlingame",
                            state="CA",
                            zipcode="94010")

    kitty_location = Location(location_id=102,
                            pet_id=102,
                            location_name="Starbucks",
                            address="54 E 4th Avenue",
                            city="San Mateo",
                            state="CA",
                            zipcode="94401")

    db.session.add_all([alice, betty, fido, kitty, fido_location, kitty_location])
    db.session.commit()


#---------------------------------------------------------------------#
#------------------- Connect to Database Section ---------------------#
#---------------------------------------------------------------------#

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