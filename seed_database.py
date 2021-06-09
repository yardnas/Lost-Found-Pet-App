import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb lost_found_pets")
os.system("createdb lost_found_pets")

model.connect_to_db(server.app)
model.db.create_all() # Create the tables defined 


# Create 5 users
for n in range(5):
    fname = f'fname{n}'
    lname = f'lname{n}'
    email = f'user{n}@test.com'
    password = 'test'

    user = crud.create_user(fname, lname, email, password)