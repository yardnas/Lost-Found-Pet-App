"""Server for the lost and found pet app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
from jinja2 import StrictUndefined
import crud


app = Flask(__name__)
app.secret_key = '89qhfhje&*djfka8238420*2i#6'
app.jinja_env.undefined = StrictUndefined

#---------------------------------------------------------------------#

@app.route('/')
def display_homepage():
    """Show the homepage."""

    return render_template('homepage.html')

@app.route('/signup')
def display_sign_up():
    """Show the sign-up page to create an account"""

    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
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


@app.route('/signin')
def display_sign_in():
    """Show the signin page to login."""

    return render_template('signin.html')


@app.route('/signin', methods=['POST'])
def process_login():
    """Log user in."""

    email = request.form["email"]
    password = request.form["password"]

    user = crud.get_user_by_email(email)

    # # TODO: Investigate why this doesn't work as expected
    # # Get value from first name for Jinja template
    # fname = crud.get_fname_by_email(email) # tuple: ('Alice',)
    # fname = fname[0] #'Alice'

    if not user:
        flash("Email does not exist. Please try again.")
        return redirect('/')

    if user.password != password:
        flash("Oops. Password is invalid. Please try again.")
        return redirect('/')

    session["logged_user_in"] = user.email
    flash("You have logged in succesfully.")

    return redirect('/welcome')

    # # TODO: Investigate why this doesn't work as expected
    # # Not functioning properly. Need to redirect and render with variable.
    # return render_template("welcome.html", name=fname) 


@app.route('/signout') # TODO
def logout():
    """Log user out."""

    #TODO: Not implemented yet

    del session["logged_user_in"]

    flash("Logged out successfully.")

    return redirect("/")


@app.route('/welcome')
def welcome():
    """Show the welcome page."""

    return render_template('welcome.html')


@app.route('/map')
def display_map():
    """Placeholder for map-related code."""

    return render_template("map.html")


#---------------------------------------------------------------------#

if __name__ == '__main__':

    connect_to_db(app)

    app.run(host='0.0.0.0', debug=True)