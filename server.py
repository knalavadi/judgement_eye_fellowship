"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register', methods=['GET'])
def register_form():
    """Renders template only."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Redirects to homepage after submission for registered users."""

    email = request.form.get("email")
    password = request.form.get("password")

    db_user = User.query.filter(email == email).first()
    db_password = User.query.filter(password == password).first()

    if db_user.email == email:
        
        if db_password == password:
            session["user"] = email #keeps track of who logged in
            flash("successfully logged in")
            return redirect("/")
        
        else:
            flash("Password is incorrect.")
            return redirect('/register')

    else:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

    return redirect("/")

    render_template("base.html")

# @app.route("/logged_out")
# def logged_out_process():

@app.route('/user_details')
def user_details():
    """Show details of a user."""

    active_user = session["user"] 

    user=User.query.filter(email = active_user).first()

    return render_template("user_details.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.run(debug=True, host='127.0.0.1')
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
