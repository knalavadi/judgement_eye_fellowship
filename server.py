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
    """Register form for new users."""
    
    username = request.args.get("username")
    password = request.args.get("password")

    if (new_user = db.session.query(User.email == username)) and 
        (db.session.query(User.password == password)):

    else:
        db.session.add(username)
        db.session.add(password)
        db.session.commit()

    return render_template("register_form.html",
                            username=username,
                            password=password,
                            new_user=new_user)


@app.route('/register', methods=['POST'])
def register_process():
    """Redirects to homepage after submission for registered users."""

    username = request.form.get("username")
    password = request.form.get("password")

    registered_user = db.session.query(User.user_id, User.password).all()

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.run(debug=True, host='127.0.0.1')
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
