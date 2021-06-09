"""CRUD (Create, Read, Update, Delete) operations."""

from model import db, User, Pet, Status, Location, connect_to_db

# Data model Classes
    # User
    # Pet
    # Status
    # Location

#---------------------------------------------------------------------#

def create_user(fname, lname, email, password): #y
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_users():
    """Return all the users."""

    return User.query.all() # [<User user_id=1 fname=Alice lname=Apple>, <User user_id=2 fname=Betty lname=Baker>]


def get_user_by_id(user_id):
    """Return a user by their user_id (primary key)."""

    return User.query.get(user_id) # <User user_id=1 fname=Alice lname=Apple>


def get_user_by_email(email):
    """"Return a user by their email address."""

    return User.query.filter(User.email == email).first() # <User user_id=2 fname=Betty lname=Baker>


def get_fname_by_email(email):
    """"Return a user by their first name."""

    # return User.query.filter(User.fname == fname).first()  # <User user_id=2 fname=Betty lname=Baker>
    return db.session.query(User.fname).filter(User.email == email).first()


def create_pets():
    """Create and return a pet."""

    pet = Pet(pet_name=pet_name, pet_type=pet_type, pet_breed=pet_breed, 
                pet_gender=pet_gender, pet_desc=pet_desc, lost_found=lost_found,
                status_id=status_id)

    db.session.add(pet)
    db.session.commit()

    return pet


def create_status():
    """Create the status of the respective pet"""

    status = Status(status=status, location_id=location_id)

    db.session.add(status)
    db.session.commit()


def create_location():
    """Create the location of the respective pet/status"""

    location = Location(location_name=location_name, address=address, city=city, 
                        state=state, zipcode=zipcode, phone_number=phone_number)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)