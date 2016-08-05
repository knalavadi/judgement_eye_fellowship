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

@app.route('/logout')
def logged_out():

    del session["user"]
    return redirect('/')


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
    print "EMAIL ", email
    password = request.form.get("password")

    user = User.query.filter(User.email == email).first()
    print "USER ", user

    if user == None:
        user = User(email=email, password=password)
        print "HERE"
        db.session.add(user)
        db.session.commit()
        session["user"] = email
        return redirect("/")

    elif User.password == password:
        session["user"] = email #keeps track of who logged in
        flash("Successfully logged in.")
        return redirect("/")

    else:
        flash("Password is incorrect.")
        return redirect('/register')

    return render_template("base.html")


@app.route('/user_details')
def user_details():
    """Show details of a user."""

    email = session["user"]

    #filter by email in User class, not DB
    #list of all movies user has rated
    user_info = User.query.filter(User.email == email).first()
    user_id = user_info.user_id
    user_ratings = Rating.query.filter(Rating.user_id == user_id).all()

    return render_template("user_details.html", user_ratings=user_ratings)


@app.route('/movies')
def movie_title_list():
    """Show movie titles"""

    movies_in_my_DB = Movie.query.order_by(Movie.title).all() #binding query to a variable
    return render_template("movie_list.html", movies=movies_in_my_DB)


@app.route('/movie_ratings/<int:movieid>')
def get_movie_ratings(movieid):
    """Show all ratings for the selected movie."""

    scores = Rating.query.filter(Rating.movie_id == movieid).all()
    title = Movie.query.get(movieid).title

    return render_template("movie_detail_ratings.html", scores=scores, title=title)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.run(debug=True, host='127.0.0.1')
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
