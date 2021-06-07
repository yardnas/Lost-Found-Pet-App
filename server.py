"""Server for the lost and found pet app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
from jinja2 import StrictUndefined
import crud


app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Show the homepage."""

    return render_template('index.html')


@app.route('/users')
def all_users():
    """Show all users."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    full_name = request.form.get('full_name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        flash('Email already exist. Please log in or try again.')
    else:
        # crud.create_user(full_name, phone_number, email, password)
        crud.create_user(full_name, email, password)
        flash('Account has been successfully created. Welcome! Please log in.')

    return redirect('/') # redirect back to homepage


@app.route('/user/<user_id>')
def show_user(user_id):
    """Display user's details"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""
    email = request.form["email"]
    password = request.form["password"]

    user = crud.get_user_by_email(email)

    if user:
        flash('You have successfully logged in.')
    else:
        crud.create_user(full_name, email, password)
        flash('Email does not exist. Please try again or sign up.')

    return redirect('/welcome')


@app.route('/logout')
def logout():
    """Process log out"""

    #TODO

    return redirect("/login")


@app.route('/welcome')
def welcome():
    """Show the welcome page."""

    return render_template('welcome.html')


if __name__ == '__main__':

    connect_to_db(app)

    app.run(host='0.0.0.0', debug=True)