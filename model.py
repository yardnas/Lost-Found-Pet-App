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


    # To handle: NotImplementedError: No 'id' attribute - override 'get_id'
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

    pet_owner = db.Column(db.String(50), nullable=False) 
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

        return f"<Pet pet_id={self.pet_id} pet_name={self.pet_name} pet_type={self.pet_type} pet_owner={self.pet_type}>"


class Status(db.Model):
    """Data model for the status of the pet."""

    __tablename__ = "status"

    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'))

    status_type = db.Column(db.String(50), nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Add relationship between users and pets
    pets = db.relationship("Pet", backref="status")

    def __repr__(self):
        """Show information about the pet."""

        return f"<Status status_id={self.status_id} pet_id={self.pet_id} status_type={self.status_type}>"


#### Location breakdwoen not needed 
# with Google Map API, able to enter full address and location
#
# class Location(db.Model):
#     """Data model for the location of the pet lost or found."""

#     __tablename__ = "locations"

#     location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'))

#     location_name = db.Column(db.String(255), nullable=True)
#     address = db.Column(db.String(100), nullable=True)
#     city = db.Column(db.String(100), nullable=True)
#     state = db.Column(db.String(50), nullable=True)
#     zipcode = db.Column(db.String(20), nullable=True)

#     # # # Add relationship between pets and locations
#     pets = db.relationship("Pet", backref="location")


    # def __repr__(self):
    #     """Show information about the location of the lost or found pet."""

    #     return f"<Location location_id={self.location_id} location_name={self.location_name} phone_number={self.city}"


#---------------------------------------------------------------------#
#------------------------ Sample Data Section ------------------------#
#---------------------------------------------------------------------#

def test_data():
    """Create sample data for testing"""

    # Empty existing data in case this is executed more than once
    User.query.delete()
    Pet.query.delete()

    # Add sample users data
    cathy = User(user_id=103, 
                fname="Cathy",
                lname="Cake",
                phone="415-777-1234",
                email="cathy@cathy.com",
                password="cathy")

    david = User(user_id=104, 
                fname="David", 
                lname="Decker",
                phone="415-777-5678", 
                email="david@david.com",
                password="david")

    spike = Pet(pet_id=203, 
                user_id=103,
                status_id=303,
                pet_owner="Cathy Cake",
                pet_name="Spike", 
                pet_type="Dog",
                pet_breed="Pitbull",
                pet_gender="Male",
                pet_color="White with brown spots",
                pet_image="/static/img/dog_pit.jpg",
                last_address="2000 El Camino Real, Palo Alto, CA 94306")

    tiger = Pet(pet_id=204,
                user_id=104,
                status_id=304,
                pet_owner="David D.",
                pet_name="Tiger",
                pet_type="Cat",
                pet_breed="American Bobtail",
                pet_gender="Male", 
                pet_color="Tiger stripes",
                pet_image="/static/img/cat_tiger.jpg",
                last_address="Golden Gate Bridge")

    spike_status = Status(status_id=303,
                pet_id=203,
                status_type="Lost")

    tiger_status = Status(status_id=304,
                pet_id=204,
                status_type="Found")


    db.session.add_all([cathy, david, spike, tiger, spike_status, tiger_status])
    db.session.commit()

#---------------------------------------------------------------------#
#------------------- Connect to Database Section ---------------------#
#---------------------------------------------------------------------#

# def connect_to_db(flask_app):
#     """Connect the database to the Flask app."""

#     flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lost_found_pets'
#     flask_app.config['SQLALCHEMY_ECHO'] = False
#     flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#     db.app = flask_app
#     db.init_app(flask_app)

#     print('Connected to the db!')

def connect_to_db(app, db_uri="postgresql:///lost_found_pets"):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

    print("Connected to thhe db!")
    
#---------------------------------------------------------------------#


if __name__ == "__main__":

    from server import app

    # from flask import Flask
    # app = Flask(__name__)

    # Connect to the database
    connect_to_db(app)
    print("Connected to DB.")

    # # Create all tables
    # db.create_all()

    # # Insert sample data (adding here for now. will move to tests.py)
    # test_data()