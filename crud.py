"""CRUD operations."""

from model import db, User, Pet, Status, Location, connect_to_db

# Define the following functions
    # crud.get_users()
    # crud.get_user_by_email(email)
    # crud.create_user(email, password)
    # crud.get_user_by_id(user_id)

# Data model Classes
    # User
    # Pet
    # Status
    # Location


def create_user(full_name, phone_number, email, password):
    """Create and return a new user."""

    user = User(full_name=full_name, phone_number=phone_number,
                email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_users():
    """Return all the users."""

    return User.query.all() 
    #[<User user_id=1 first_name=Alice last_name=Apple>, 
    # <User user_id=2 first_name=Betty last_name=Baker>]


def get_user_by_id(user_id):
    """Return a user by their user_id (primary key)."""

    return User.query.get(user_id)
    # <User user_id=1 first_name=Alice last_name=Apple>


def get_user_by_email(email):
    """"Return a user by their email address."""

    return User.query.filter(User.email == email).first()
    # <User user_id=2 first_name=Betty last_name=Baker>


if __name__ == "__main__":

    from server import app
    connect_to_db(app)