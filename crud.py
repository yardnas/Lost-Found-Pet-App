"""CRUD (Create, Read, Update, Delete) operations."""

from model import db, User, Pet, connect_to_db

#---------------------------------------------------------------------#
#------------------ CRUD functions for USERS Section -----------------#
#---------------------------------------------------------------------#

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, 
                lname=lname, 
                email=email, 
                password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_users():
    """Return all the users."""

    return User.query.all() # [<User user_id=1 fname=Alice lname=Apple>]


def get_user_by_id(user_id):
    """Return a user by their user_id (primary key)."""

    return User.query.get(user_id) 

def get_user_by_email(email):
    """"Return a user by their email address."""

    return User.query.filter(User.email == email).first() 


def get_fname_by_email(email):
    """"Return a user by their first name."""

    return db.session.query(User.fname).filter(User.email == email).first()


#---------------------------------------------------------------------#
#------------------ CRUD functions for PETS Section ------------------#
#---------------------------------------------------------------------#

def create_pet(pet_name, pet_type, pet_breed, pet_gender, 
                pet_color, pet_status, pet_image, last_address):
    """Create and return a pet."""

    pet = Pet(pet_name=pet_name,
              pet_type=pet_type, 
              pet_breed=pet_breed, 
              pet_gender=pet_gender,
              pet_color=pet_color,
              pet_status=pet_status,
              pet_image=pet_image,
              last_address=last_address)

    db.session.add(pet)
    db.session.commit()

    return pet


def register_pet_user(email, phone, pet_name, pet_type, pet_breed, 
                         pet_gender, pet_color, pet_status, pet_image, last_address):
    """Update pet and pet owner's information"""

    # TODO: revisit logic
    #
    user = get_user_by_email(email)
    user_id = user.user_id

    pet = create_pet(pet_name, pet_type, pet_breed, pet_gender, pet_color, pet_status, pet_image, last_address)
    pet_id = pet.pet_id

    # Update user section
    user_update= User.query.filter(User.email==email).update({User.phone: phone})

    # Update pet section
    pet_update = Pet.query.filter(Pet.pet_id==pet_id).update({Pet.user_id: user_id, Pet.pet_status: pet_status})

    db.session.commit()

    return pet_update


def update_pet_status(email, pet_name, pet_status):
    """Update pet status when pet is found."""

    user_id = db.session.query(User.user_id).filter(User.email==email, Pet.pet_name==pet_name).first()

    # Update the status of the pet
    status_update = db.session.query(Pet).filter(Pet.user_id == user_id, Pet.pet_name == pet_name).update({Pet.pet_status: pet_status})
    
    db.session.commit()

    return status_update


def get_pet_user_info():
    """Get pet and pet owner's information"""

    return db.session.query(User.email, Pet.pet_name, Pet.pet_type, Pet.pet_breed, 
                                 Pet.pet_color, Pet.pet.status, Pet.last_address).filter(User.user_id == Pet.user_id).all()
    

#---------------------------------------------------------------------#


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
