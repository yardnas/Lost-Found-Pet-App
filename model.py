"""Models for the Neighborhood Lost Pets app."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin # for flask-login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

#---------------------------------------------------------------------#
#------------------------ Project Scope Section ----------------------#
#---------------------------------------------------------------------#
# Data Model 
    # √ User can have many Pets
    # √ Pet can have one owner
    # X (omitted Status, instead added status to Pet)
    # X (omitted Location, instead added address to Pet)

# MVP
    # √ Sign-up | Sign-in | Log-out => used flask-login to achieve
    # √ Store pet info (desc, pics, location) => stored in postgres db
    # √ Show pet location on the map => utilize the google maps api
    # √ Show pet & pet owner info on markers => AJAX-josonify-map.js
    # √ Handle lost and found pets => forms

# Nice-to-have
    # √ Dynamically pin location by entering location (opposed to filling out the registration page)
    # √ Add Night mode (map)
    # √ Add form/page/db to handle found pets
    #   Add messaging/chat feature

#---------------------------------------------------------------------#
#------------------------- Data Model Section ------------------------#
#---------------------------------------------------------------------#

class User(db.Model, UserMixin):
    """Data model for the user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # To handle: NotImplementedError: No 'id' attribute - override 'get_id'
    def get_id(self):
           return (self.user_id)
    
    # To display information about the user when querying
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
    pet_status = db.Column(db.String(50), nullable=True)
    pet_image = db.Column(db.String(50), nullable=True)
    last_address = db.Column(db.String(100), nullable=False)

    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Add relationship between users and pets
    users = db.relationship("User", backref="pet")

    # To display information about the pet when querying
    def __repr__(self):
        """Show information about the pet."""

        return f"<Pet pet_id={self.pet_id} pet_name={self.pet_name} pet_type={self.pet_type} pet_status={self.pet_status}>"


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
                pet_name="Spike", 
                pet_type="Dog",
                pet_breed="Pitbull",
                pet_gender="Male",
                pet_color="White with brown spots",
                pet_status="Lost",
                pet_image="/static/img/dog_pit.jpg",
                last_address="2000 El Camino Real, Palo Alto, CA 94306")

    tiger = Pet(pet_id=204,
                user_id=104,
                pet_name="Tiger",
                pet_type="Cat",
                pet_breed="American Bobtail",
                pet_gender="Male", 
                pet_color="Tiger stripes",
                pet_status="Lost",
                pet_image="/static/img/cat_tiger.jpg",
                last_address="Golden Gate Bridge")

    db.session.add_all([cathy, david, spike, tiger])
    db.session.commit()

#---------------------------------------------------------------------#
#------------------- Connect to Database Section ---------------------#
#---------------------------------------------------------------------#

def connect_to_db(app, db_uri="postgresql:///lost_found_pets"):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

    print("Connected to the db!")
    
#---------------------------------------------------------------------#

if __name__ == "__main__":

    from server import app

    # Connect to the database
    connect_to_db(app)
