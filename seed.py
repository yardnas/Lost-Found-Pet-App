"""Seed data to jump start the app with data."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
from model import db, connect_to_db, User, Pet
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
            password="$2b$12$8eeLrg3KjAG5LfK5dLRv1OOq3aT7bjVHSleLOaRr9xu7Mt3xpo4py")

winston = Pet(pet_id=201, 
            user_id=101,
            pet_name="Winston", 
            pet_type="Dog",
            pet_breed="Bulldog",
            pet_gender="Male",
            pet_color="White with blk spots on ears",
            pet_status="Lost",
            pet_image="/static/img/dog_bulldog.jpg",
            last_address="5455 Geary Blvd, San Francisco, CA 94121")

bobby = User(user_id=102, 
            fname="Bobby", 
            lname="Baker",
            phone="415-555-5678", 
            email="bobby@bobby.com",
            password="$2b$12$diL5A03FLtXQUmlVULYfYuJPJwcelXK/XpiGhF8T/jy3UB1oC9EFW")

kitty = Pet(pet_id=202,
            user_id=102,
            pet_name="Kitty",
            pet_type="Cat",
            pet_breed="British Shorthair",
            pet_gender="Female", 
            pet_color="Grey with orange eyes",
            pet_status="Lost",
            pet_image="/static/img/cat_grey.jpg",
            last_address="1230 Broadway, Burlingame, CA 94010")

cathy = User(user_id=103, 
            fname="Cathy",
            lname="Cake",
            phone="415-777-1234",
            email="cathy@cathy.com",
            password="$2b$12$f0U95Ng3Atxgx23j7fsTEeROSv.HOYYB6iQBMzrP59wgNzK.lq9l.")

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

david = User(user_id=104, 
            fname="David", 
            lname="Decker",
            phone="415-777-5678", 
            email="david@david.com",
            password="$2b$12$DfVmMZhCGj13xy7Cf4fSveGx14c54K4Et6L0O9bRjK74QgyyiQSiy")

tiger = Pet(pet_id=204,
            user_id=104,
            pet_name="Tiger",
            pet_type="Cat",
            pet_breed="American Bobtail",
            pet_gender="Male", 
            pet_color="Tiger stripes",
            pet_status="Lost",
            pet_image="/static/img/cat_tiger.jpg",
            last_address="1501 Fillmore St, San Francisco, CA 94115")

evan = User(user_id=105, 
            fname="Evan", 
            lname="Eats",
            phone="415-777-1111", 
            email="evan@evan.com",
            password="$2b$12$.jm6Ag0OAhl5r1OmeIfo5eKFSRZ66ClcgElftcIqWI7.7BhxfttU2")

cloud = Pet(pet_id=205,
            user_id=105,
            pet_name="Cloud",
            pet_type="Dog",
            pet_breed="Bichon",
            pet_gender="Female", 
            pet_color="White",
            pet_status="Lost",
            pet_image="/static/img/dog_bichon.jpg",
            last_address="1899 Union St, San Francisco, CA 94123")

fanny = User(user_id=106, 
            fname="Fanny", 
            lname="Fancy",
            phone="415-777-2222", 
            email="fanny@fanny.com",
            password="$2b$12$nitMTtP/8dhWEvs/pqMqjOcT7I.2cHwmZUW/kDy1HERN3JU5kFDKW")

bear = Pet(pet_id=206,
            user_id=106,
            pet_name="Bear",
            pet_type="Dog",
            pet_breed="Chow chow",
            pet_gender="Male", 
            pet_color="Brown",
            pet_status="Lost",
            pet_image="/static/img/dog_chowchow.jpg",
            last_address="693 Santa Cruz Ave, Menlo Park, CA 94025")

george = User(user_id=107, 
            fname="George", 
            lname="Great",
            phone="415-777-3333", 
            email="george@george.com",
            password="$2b$12$nkQ.hF9Y.mrKms9P9.4MTO.siEvLOQ2eVHaqMSracoVakV/l19SZO")

blue = Pet(pet_id=207,
            user_id=107,
            pet_name="Blue",
            pet_type="Cat",
            pet_breed="Ragdoll",
            pet_gender="Male", 
            pet_color="White w/brown face & blue eyes",
            pet_status="Lost",
            pet_image="/static/img/cat_ragdoll.jpg",
            last_address="1000 Metro Center Blvd E, Foster City, CA 94404")

#---------------------------------------------------------------------#

model.db.session.add_all([alice, bobby, winston, kitty, cathy, david, spike, tiger, evan, cloud, fanny, bear, george, blue])
model.db.session.commit()