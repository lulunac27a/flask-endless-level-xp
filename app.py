"""
A simple Flask application for a user with level and XP (experience points) system.
"""

import math
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)


class User(db.Model):  # user class
    """
    A user model to store the level and experience points (XP).
    """

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)  # user id
    username = db.Column(db.String(80), unique=True, nullable=False)  # username
    xp = db.Column(db.Float, default=0)  # user XP
    xp_required = db.Column(db.Float, default=1)  # user XP required
    total_xp = db.Column(db.Float, default=0)  # user total XP
    level = db.Column(db.Integer, default=1)  # user level

    def add_xp(self, amount):  # add XP
        """
        Add XP (experience points) to the user.
        amount - the amount to add XP.
        """
        self.xp += amount  # add XP by amount
        self.total_xp += amount  # add total XP by amount
        self.check_level_up()  # check if user has leveled up

    def check_level_up(self):  # check if user has leveled up
        """
        Check if the user has leveled up.
        """
        while (
            self.xp >= self.xp_required
        ):  # if user XP is greater than or equal to XP required
            self.xp -= self.xp_required
            self.xp_required = round(
                self.xp_required + self.xp_required * 1 / math.sqrt(self.level)
            )
            self.level += 1  # increase level

    def get_xp_required(self):  # get required XP to next level
        """
        Get the required XP for the user to level up.
        """
        return self.xp_required

    def get_level_progress(self):  # get level progress
        """
        Get the level progress as a percentage.
        """
        return (self.xp / self.xp_required) * 100


@app.template_filter("short_numeric")  # short numeric filter
def short_numeric_filter(value):  # get number in short numeric form with abbreviations
    """
    Get the abbreviated numeric value.
    value - the numeric value to convert.
    """
    units = [
        "",
        "K",
        "M",
        "B",
        "T",
        "Qa",
        "Qi",
        "Sx",
        "Sp",
        "O",
        "N",
        "D",
        "UD",
        "DD",
        "TD",
        "QaD",
        "QiD",
        "SxD",
        "SpD",
        "OD",
        "ND",
        "V",
    ]  # list of units with abbreviations
    exponent = 0
    mantissa = value  # mantissa value from 1 to 999
    while mantissa >= 1000:  # repeat until mantissa is within 1 to 999
        mantissa /= 1000
        exponent += 1
    return (
        f"{mantissa:.3g}{units[exponent]}" if value >= 1000 else f"{value:.0f}"
    )  # print abbreviated output


app.jinja_env.filters["short_numeric"] = short_numeric_filter  # add filter to Jinja


@app.route("/")  # index page
def index():  # get index page template
    """
    Return the index page containing a user.
    """
    user = User.query.first()  # get first user
    return render_template("index.html", user=user)  # return index page template


@app.route("/add_xp", methods=["POST"])  # add XP from POST method
def add_xp():  # add XP
    """
    Add XP (experience points) based on entered amount.
    """
    user = User.query.first()  # get first user
    user.add_xp(float(request.form["amount"]))  # parse amount as float
    db.session.commit()  # commit database changes
    return redirect(url_for("index"))  # return index page template


def init_db():  # initialize database
    """
    Initialize the user database.
    """
    with app.app_context():
        db.create_all()  # initialize database
        if User.query.count() == 0:  # if there is no user in database
            new_user = User(username="Player")  # add user with name 'Player'
            db.session.add(new_user)  # add new user to database
            db.session.commit()  # commit database changes


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=8081)  # run the app at post 8081
