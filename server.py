"""Server for the lost and found pet app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from model import connect_to_db, db, Pet, User, Status
from jinja2 import StrictUndefined
import crud

app = Flask(__name__)
app.secret_key ='secret_key'
app.jinja_env.undefined = StrictUndefined

# Create LoginManager and attach to the Flask app instance
#
login_manager = LoginManager()
login_manager.init_app(app)

#---------------------------------------------------------------------#
#-------------------- Route for Welcome Page -------------------------#
#---------------------------------------------------------------------#

@app.route('/')
def display_welcome():
    """Show the welcome page."""

    return render_template('index.html')


#---------------------------------------------------------------------#
#--------- Routes for User Login | Register | Logout Section ---------#
#---------------------------------------------------------------------#

# Define callback function for login_manager.user_loader
#
@login_manager.user_loader
def load_user(user_id):
    """Takes in user_id and return a User instance."""

    # return User.query.get(user_id)
    return crud.get_user_by_id(user_id)


@app.route('/login')
def display_login():
    """Show the signin page to login."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Log user in."""

    email = request.form['email']
    password = request.form['password']

    user = crud.get_user_by_email(email)

    if not user:
        flash('Email does not exist. Please try again.')
        return redirect('/')

    if user.password != password:
        flash('Oops. Password is invalid. Please try again.')
        return redirect('/')

    # Call flask_login.login_user to login a user
    login_user(user)

    flash('You have logged in succesfully.')

    return redirect('/dashboard')


@app.route('/register')
def register_user():
    """Show the register page to create an account."""

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def create_user():
    """Register a new user."""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        flash('Email already exist. Please log in or try again.')
    else:
        crud.create_user(fname, lname, email, password)
        flash('Account has been successfully created. Please login')

    return redirect('/') # redirect back to homepage


@app.route('/logout')
@login_required
def logout():
    """Logout user."""

    logout_user()
    # del session["logged_user_in"]

    flash('Logged out successfully.')

    return redirect('/')


#---------------------------------------------------------------------#
#------------- Routes for Main Page (Dashboard) Section --------------#
#---------------------------------------------------------------------#

@app.route('/dashboard')
@login_required
def welcome():
    """Show the welcome dashboard."""

    return render_template('dashboard.html')

# Don't think I need this since there is a POST for pet_register
#
# @app.route('/dashboard', methods=['POST'])
# @login_required
# def create_pet_registration():
#     """Store pet location in database and redirect back to dashboard"""

#     return redirect('dashboard')


#---------------------------------------------------------------------#
#----------- Routes for Pet Info & Registration Section --------------#
#---------------------------------------------------------------------#

@app.route('/pet_register')
@login_required
def show_pet_registration():
    """Show the pet registration page by rendering the page."""

    return render_template('pet_register.html')


@app.route('/pet_register', methods=['POST'])
@login_required
def register_pet_form():
    """To fill out the pet registration form, store in db and redirect back to '/'."""

    pet_owner = request.form.get('pet-owner')
    email = request.form.get('email')
    phone = request.form.get('phone')
    pet_name = request.form.get('pet-name')
    pet_type = request.form.get('pet-type')
    pet_breed = request.form.get('pet-breed')
    pet_gender = request.form.get('pet-gender')
    pet_color = request.form.get('pet-color')
    pet_image = request.form.get('pet-image')
    last_address = request.form.get('last-address')

    user = crud.get_user_by_email(email)

    # Update database with pet & owner's information
    if user:
        flash('Pet registration is complete')
        crud.update_pet_user_info(pet_owner, email, phone, 
                        pet_name, pet_type, pet_breed, 
                        pet_gender, pet_color, pet_image, last_address)
    if not user:
        flash('Oops. Please register first and try again')
        return redirect('/')

    # return render_template('dashboard.html')
    return redirect('dashboard')


#---------------------------------------------------------------------#

@app.route('/api/pets')
@login_required
def get_all_pets():
    """Return JSON information about pets for marker info content."""

    pet_info = db.session.query(User.email, User.fname, Pet.pet_name, Pet.pet_type, Pet.pet_breed, Pet.pet_color, Pet.pet_image, Pet.last_address).filter(User.user_id == Pet.user_id).all()

    pets = []

    for idx, pet in enumerate(pet_info):
        info = {
            'userEmail': pet_info[idx][0],
            'petOwner': pet_info[idx][1],
            'petName': pet.pet_name,
            'petType': pet.pet_type,
            'petBreed': pet.pet_breed,
            'petColor': pet.pet_color,
            'petImage': pet.pet_image,
            'lastAddress': pet.last_address
        }
        pets.append(info)

    return jsonify(pets)


@app.route('/pet_owner')
@login_required
def display_petowner():
    """Pet owner's page for view into owner's pet info"""

    return render_template('pet_owner.html')


@app.route('/search')
@login_required
def search_info():
    """Search bar and search results"""

    return render_template('search.html')


#---------------------------------------------------------------------#

if __name__ == '__main__':

    connect_to_db(app)

    app.run(host='0.0.0.0', debug=True)