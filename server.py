"""Server for the lost and found pet app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from model import connect_to_db, db, Pet
from jinja2 import StrictUndefined
import crud

app = Flask(__name__)
app.secret_key = '89qhfhje&*djfka8238420*2i#6'
app.jinja_env.undefined = StrictUndefined

# Create LoginManager and attach to the Flask app instance
login_manager = LoginManager()
login_manager.init_app(app)

#---------------------------------------------------------------------#

@app.route('/')
def display_splash():
    """Show the splash page."""

    return render_template('index.html')

# Define callback function for login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    """Takes in user_id and return a User instance"""

    # return User.query.get(user_id)
    return crud.get_user_by_id(user_id)


@app.route('/login')
def display_login():
    """Show the signin page to login."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Log user in."""

    email = request.form["email"]
    password = request.form["password"]

    user = crud.get_user_by_email(email)

    if not user:
        flash("Email does not exist. Please try again.")
        return redirect('/')

    if user.password != password:
        flash("Oops. Password is invalid. Please try again.")
        return redirect('/')

    # session["logged_user_in"] = user.email

    # Call flask_login.login_user to login a user
    login_user(user)

    flash("You have logged in succesfully.")

    return redirect('/dashboard')


@app.route('/register')
def register_user():
    """Show the register page to create an account."""

    return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
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

    flash("Logged out successfully.")

    return redirect('/')


@app.route('/dashboard')
@login_required
def welcome():
    """Show the welcome dashboard."""

    return render_template('dashboard.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def create_lost_pet():
    """Register a lost pet"""

    fname = request.form.get('fname')
    email = request.form.get('email')
    phone = request.form.get('phone')
    pet_name = request.form.get('pet-name')
    pet_type = request.form.get('pet-type')
    pet_breed = request.form.get('pet-breed')
    pet_gender = request.form.get('pet-gender')
    pet_color = request.form.get('pet-color')
    pet_image = request.form.get('pet-image')

    user = crud.get_user_by_email(email)

    # # Update database with pet's information
    # crud.create_pets(pet_name, pet_type, pet_breed, pet_gender, pet_color, pet_image)

    # Update database with user's information
    if user:
        flash('Successfully added')
        # crud.update_user_info(fname, email, phone)
        crud.update_user_pet_info(fname, email, phone, 
                        pet_name, pet_type, pet_breed, 
                        pet_gender, pet_color, pet_image)
    else:
        flash('Please register first and try again')
        return redirect('/')

    return render_template('dashboard.html')


@app.route('/dashboard', methods=['POST'])
@login_required
def create_pet_location():
    """Store pet location in database"""

    return redirect('dashboard')


@app.route('/pet_register')
@login_required
def show_pet_registration():
    """Show the welcome dashboard."""

    return render_template('pet_register.html')


@app.route('/pet_register', methods=['POST'])
@login_required
def register_pet_form():
    """Show the register page to create an account."""

    fname = request.form.get('fname')
    email = request.form.get('email')
    phone = request.form.get('phone')
    pet_name = request.form.get('pet-name')
    pet_type = request.form.get('pet-type')
    pet_breed = request.form.get('pet-breed')
    pet_gender = request.form.get('pet-gender')
    pet_color = request.form.get('pet-color')
    pet_image = request.form.get('pet-image')

    user = crud.get_user_by_email(email)

    # Update database with user's information
    if user:
        flash('Pet registration is complete')
        crud.update_user_pet_info(fname, email, phone, 
                        pet_name, pet_type, pet_breed, 
                        pet_gender, pet_color, pet_image)
    if not user:
        flash('Oops. Please register first and try again')
        return redirect('/')

    return render_template('dashboard.html')


@app.route("/get/pets")
def pet_info():
    """JSON information about pets."""

    pets = [
        {
            "petId": pet.pet_id,
            "userId": pet.user_id,
            "petName": pet.pet_name,
            "petType": pet.pet_type,
            "petBreed": pet.pet_breed,
            "petColor": pet.pet_color,
            "petImage": pet.pet_image,
            "lastAddress": pet.last_address,
            "capLat": pet.cap_lat,
            "capLong": pet.cap_long
        }
        for pet in Pet.query.limit(50)
    ]

    return jsonify(pets)


#---------------------------------------------------------------------#

if __name__ == '__main__':

    connect_to_db(app)

    app.run(host='0.0.0.0', debug=True)