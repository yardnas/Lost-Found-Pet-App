"""CRUD (Create, Read, Update, Delete) operations."""

from model import db, User, Pet, Status, connect_to_db

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

    return User.query.all() # [<User user_id=1 fname=Alice lname=Apple>, <User user_id=2 fname=Betty lname=Baker>]


def get_user_by_id(user_id):
    """Return a user by their user_id (primary key)."""

    return User.query.get(user_id) # <User user_id=1 fname=Alice lname=Apple>


def get_user_by_email(email):
    """"Return a user by their email address."""

    return User.query.filter(User.email == email).first() # <User user_id=2 fname=Betty lname=Baker>


def get_fname_by_email(email):
    """"Return a user by their first name."""

    return db.session.query(User.fname).filter(User.email == email).first()


#---------------------------------------------------------------------#
#------------------ CRUD functions for PETS Section ------------------#
#---------------------------------------------------------------------#

def create_pets(pet_owner, pet_name, pet_type, pet_breed, pet_gender, pet_color, pet_image, last_address):
    """Create and return a pet."""

    pet = Pet(pet_owner=pet_owner, 
              pet_name=pet_name,
              pet_type=pet_type, 
              pet_breed=pet_breed, 
              pet_gender=pet_gender,
              pet_color=pet_color,
              pet_image=pet_image,
              last_address=last_address)

    db.session.add(pet)
    db.session.commit()

    return pet


def update_pet_user_info(pet_owner, email, phone, 
                         pet_name, pet_type, pet_breed, 
                         pet_gender, pet_color, pet_image, last_address):
    """Update pet and pet owner's information"""

    # TODO: 
        # Not sure about this logic since its updating "id"
        # Get review for correctness and efficiency

    user = get_user_by_email(email)
    user_id = user.user_id

    # TODO: Fix this to query db for pet_id opposed to using the create function
    pet = create_pets(pet_owner, pet_name, pet_type, pet_breed, 
                      pet_gender, pet_color, pet_image, last_address)

    pet_id = pet.pet_id

    # Update user section
    # user_update= User.query.filter(User.email==email).update({User.fname: fname, User.phone: phone})
    user_update= User.query.filter(User.email==email).update({User.phone: phone})

    # Update pet section
    pet_update = Pet.query.filter(Pet.pet_id==pet_id).update({Pet.user_id: user_id, Pet.pet_owner: pet_owner})

    db.session.commit()

    return pet_update


def get_pet_user_info():
    """Get pet and pet owner's information"""

    # pet_user = db.session.query(User.email, Pet.pet_name, Pet.pet_type, Pet.pet_breed, 
    #                             Pet.pet_color, Pet.last_address).filter(User.user_id == Pet.user_id).all()

    # return pet_user
    return db.session.query(User.email, Pet.pet_name, Pet.pet_type, Pet.pet_breed, 
                                 Pet.pet_color, Pet.last_address).filter(User.user_id == Pet.user_id).all()
    

#---------------------------------------------------------------------#
#---------------- CRUD functions for STATUS section ------------------#
#---------------------------------------------------------------------#

# TODO: Work on this with the Pet Owner's Page and Search Functinality


#---------------------------------------------------------------------#


if __name__ == "__main__":

    from server import app
    connect_to_db(app)

    # result = User.query.join(Pet).all()
    # db.session.query(User, Pet).all()


    # db.session.query(User, Pet).filter(User.user_id == Pet.user_id).all()

    # [(<User user_id=101 email=alice@alice.com fname=Alice>, <Pet pet_id=201 pet_name=Fido pet_type=Dog pet_owner=Dog>), 
    # (<User user_id=102 email=bobby@bobby.com fname=Bobby>, <Pet pet_id=202 pet_name=Kitty pet_type=Cat pet_owner=Cat>), 
    # (<User user_id=101 email=alice@alice.com fname=Alice>, <Pet pet_id=1 pet_name=Pokemon pet_type=Dog pet_owner=Dog>), 
    # (<User user_id=1 email=david@david.com fname=David>, <Pet pet_id=2 pet_name=Spike pet_type=Dog pet_owner=Dog>), 
    # (<User user_id=2 email=evan@evan.com fname=Evan>, <Pet pet_id=3 pet_name=Tiger pet_type=Cat pet_owner=Cat>), 
    # (<User user_id=101 email=alice@alice.com fname=Alice>, <Pet pet_id=4 pet_name=Pokemon pet_type=Dog pet_owner=Dog>)]


    #db.session.query(User.email, Pet.pet_name, Pet.pet_breed, Pet.last_address).filter(User.user_id == Pet.user_id).all()

    # [('alice@alice.com', 'Fido', 'Bulldog', '54 E 4th Ave, San Mateo, CA 94401'), 
    # ('bobby@bobby.com', 'Kitty', 'British Shorthair', '1230 Broadway, Burlingame, CA 94010'), 
    # ('alice@alice.com', 'Pokemon', 'Golden Retriever', '2000 El Camino Real, Palo Alto, CA 94306'), 
    # ('david@david.com', 'Spike', 'Pitbull', '689 Townsend St, San Francisco, CA 94103 '), 
    # ('evan@evan.com', 'Tiger', 'Unknown', '525 El Camino Real, Millbrae, CA 94030'), ,
    # ('alice@alice.com', 'Pokemon', 'Golden Retriever', '2000 El Camino Real, Palo Alto, CA 94306')]


    # db.session.query(User.email, Pet.pet_name, Pet.pet_type, Pet.pet_breed, Pet.pet_color, Pet.last_address).filter(User.user_id == Pet.user_id).all()
    # ('alice@alice.com', 'Fido', 'Dog', 'Bulldog', 'White with blk spots on ears', '54 E 4th Ave, San Mateo, CA 94401'), 
    # ('bobby@bobby.com', 'Kitty', 'Cat', 'British Shorthair', 'Grey with orange eyes', '1230 Broadway, Burlingame, CA 94010'), 
    # ('alice@alice.com', 'Pokemon', 'Dog', 'Golden Retriever', 'Brown', '2000 El Camino Real, Palo Alto, CA 94306'), 
    # ('david@david.com', 'Spike', 'Dog', 'Pitbull', 'White w/brown brindle', '689 Townsend St, San Francisco, CA 94103 '), 
    # ('evan@evan.com', 'Tiger', 'Cat', 'Unknown', 'Tiger stripes', '525 El Camino Real, Millbrae, CA 94030'), 
    # ('alice@alice.com', 'Pokemon', 'Dog', 'Golden Retriever', 'Brown', '2000 El Camino Real, Palo Alto, CA 94306')]