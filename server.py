"""Server for the lost and found pet app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from model import connect_to_db
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
        flash('Account has been successfully created. Please sign in.')

    return redirect('/') # redirect back to homepage


@app.route('/logout')
def logout():
    """Logout user."""

    logout_user()
    # del session["logged_user_in"]

    flash("Logged out successfully.")

    return redirect("/")


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
    pet_picture = request.form.get('pet-picture')

    #user = crud.get_user_by_email(email)

    # if user:
    #     flash('Email already exist. Please log in or try again.')
    # else:
    #     crud.create_user(fname, lname, email, password)
    #     flash('Account has been successfully created. Please sign in.')

    # if user:
    #     created_user = crud.create_user(fname, lname, email, password)
    #     if created_user == None: #if some of the fields are left empty, the function create_user will return none
    #         flash("Please fill out all required fields.")
    #         return redirect("/create_account")
    #     else:   
    #         flash('Account created successfully. Please log in.')
    #         return redirect("/login")

    return redirect('/') # redirect back to homepage


@app.route('/map')
@login_required
def display_map():
    """Placeholder for map-related code."""

    return render_template("map.html")


#---------------------------------------------------------------------#

if __name__ == '__main__':

    connect_to_db(app)

    app.run(host='0.0.0.0', debug=True)