import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
from model import db, connect_to_db, User, Pet, Status
import server

os.system("dropdb lost_found_pets")
os.system("createdb lost_found_pets")

model.connect_to_db(server.app)
model.db.create_all() # Create the tables defined 


#---------------------------------------------------------------------#

# Add seed data to database
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

fido = Pet(pet_id=201, 
            user_id=101,
            pet_owner="Alice Apple",
            pet_name="Fido", 
            pet_type="Dog",
            pet_breed="Bulldog",
            pet_gender="Male",
            pet_color="White with blk spots on ears",
            pet_image="/static/img/dog_bulldog.jpg",
            last_address="54 E 4th Ave, San Mateo, CA 94401")

kitty = Pet(pet_id=202,
            user_id=102,
            pet_owner="Bobby Baker",
            pet_name="Kitty",
            pet_type="Cat",
            pet_breed="British Shorthair",
            pet_gender="Female", 
            pet_color="Grey with orange eyes",
            pet_image="/static/img/cat_grey.jpg",
            last_address="1230 Broadway, Burlingame, CA 94010")


fido_status = Status(status_id=301,
            pet_id=201,
            status_type="Lost")

kitty_status = Status(status_id=302,
            pet_id=202,
            status_type="Found")


#---------------------------------------------------------------------#

model.db.session.add_all([alice, betty, fido, kitty,  fido_status, kitty_status])
# model.db.session.add_all([alice, betty, fido, kitty])
model.db.session.commit()