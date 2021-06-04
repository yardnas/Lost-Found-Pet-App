"""Models for lost and found pets app."""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """Data model for the user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(50), nullable=True)
    #first_name = db.Column(db.String(50), nullable=True)
    #last_name = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    user_type = db.Column(db.String(50), nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Foreign key(s)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'), nullable=True)

    # Add relationship between users and pets
    #pets = db.relationship("Pet", backref="users")

    def __repr__(self):
        """Display information about the user."""


        return f"<User user_id={self.user_id}\
                        first_name={self.first_name}\
                        last_name={self.last_name}>"


class Pet(db.Model):
    """Data model for the pet."""

    __tablename__ = "pets"

    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_name = db.Column(db.String(50), nullable=True)
    pet_type = db.Column(db.String(50), nullable=True)
    pet_breed = db.Column(db.String(50), nullable=True)
    pet_gender = db.Column(db.String(20), nullable=True)
    pet_desc = db.Column(db.Text, nullable=True)
    lost_found = db.Column(db.String(20), nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Foreign key(s)
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'), nullable=True)
    #pet_image_id = db.Column(db.Integer, db.ForeignKey('pet_images.image_id'), nullable=False)

    # Add relationship between users and pets
    users = db.relationship("User", backref="pets")

    def __repr__(self):
        """Show information about the pet."""

        return f"<Pet pet_id={self.pet_id}\
                        pet_name={self.pet_name}\
                        pet_type={self.pet_type}>"


# class PetImages(db.Model):
#     # TODO: research methods to store images (cloud, text files)
    

class Status(db.Model):
    """Data model for the status of the pet."""

    __tablename__ = "status"

    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(50), nullable=True)

    #Foreign key(s)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=True)

    # Add relationship between pets and their statuses
    pets = db.relationship("Pet", backref="status")

    def __repr__(self):
        """Show information about the status of the pet."""

        return f"<Status status_id={self.status_id}\
                            status={self.status}>"


class Location(db.Model):
    """Data model for the location of the pet lost or found."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zipcode = db.Column(db.String(20), nullable=True)
    phone_number = db.Column(db.String(50), nullable=True)

    # Add relationship between status and location
    status = db.relationship("Status", backref="locations")

    def __repr__(self):
        """Show information about the location of the lost or found pet."""

        return f"<Location location_id={self.location_id}\
                            location_name={self.location_name}\
                            phone_number={self.phone_number}"


def sample_data():
    """Create sample data for testing"""

    # Empty existing data in case this is executed more than once
    User.query.delete()

    # Add sample users data
    alice = User(user_id=101, 
                pet_id=1, 
                full_name="Alice Apple",
                #first_name="Alice",
                #last_name="Apple",
                phone_number="415-555-1234",
                email="alice@alice.com",
                password="password123",
                user_type="pet_owner")

    betty = User(user_id=102, 
                pet_id=2,
                full_name="Betty Baker",
                #first_name="Betty", 
                #last_name="Baker",
                phone_number="415-555-5678", 
                email="betty@betty.com",
                password="password456", 
                user_type="reporter")

    fido = Pet(pet_id=1, 
                pet_name="Fido", 
                pet_type="Dog",
                pet_breed="Corgi",
                pet_gender="Male",
                pet_desc="Brown coat with three dark spots on the tail",
                lost_found="Lost",
                status_id=1)

    kitty = Pet(pet_id=2, 
                pet_name="Kitty",
                pet_type="Cat",
                pet_breed="British Shorthair",
                pet_gender="Female", 
                pet_desc="Gray coat with blue eyes",
                lost_found="Lost",
                status_id=2)

    fido_status = Status(status_id=1, 
                            status="Pet Found",
                            location_id=1)

    kitty_status = Status(status_id=2,
                            status="Pet Lost",
                            location_id=2)

    fido_location = Location(location_id=1,
                            location_name="Burlingame Family Pet Hospital",
                            address="1808 Magnolia Avenue",
                            city="Burlingame",
                            state="CA",
                            zipcode="94010",
                            phone_number="650-697-7234")

    kitty_location = Location(location_id=2,
                            location_name="Starbucks",
                            address="54 E 4th Avenue",
                            city="San Mateo",
                            state="CA",
                            zipcode="94401",
                            phone_number="650-548-1764")

    db.session.add_all([alice, betty, fido, kitty, fido_status, kitty_status, fido_location, kitty_location])
    db.session.commit()


def connect_to_db(flask_app):
    """Connect the database to the Flask app."""

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///lost_found_pets"
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.app = flask_app
    db.init_app(flask_app)
    print("Conneced to db!")

    print('Connected to the db!')


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