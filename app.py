"""
A simple Flask application for a user with level and XP (experience points) system.
"""

import math
from typing import Union
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, request
from flask_migrate import Migrate as MigrateClass
from flask_sqlalchemy import SQLAlchemy
from werkzeug.wrappers import Response

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)
migrate_instance = MigrateClass(app, db)


class User(db.Model):  # user class
    """
    A user model to store the level and experience points (XP).
    """

    id: int = db.Column(
        db.Integer, primary_key=True, unique=True, nullable=False
    )  # user ID
    username: str = db.Column(
        db.String(80), unique=True, nullable=False)  # username
    xp: float = db.Column(
        db.Float, default=0, server_default="0", nullable=False
    )  # user XP
    xp_required: float = db.Column(
        db.Float, default=1, server_default="1", nullable=False
    )  # user XP required
    total_xp: float = db.Column(
        db.Float, default=0, server_default="0", nullable=False
    )  # user total XP
    multiplier: int = db.Column(
        db.Integer, default=1, server_default="1", nullable=False
    )  # user multiplier
    last_item_clicked: int = db.Column(
        db.Integer, default=0, server_default="0", nullable=False
    )  # user last item clicked
    level: int = db.Column(
        db.Integer, default=1, server_default="1", nullable=False
    )  # user level
    last_time_clicked: datetime = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        server_default="CURRENT_TIMESTAMP",
        nullable=False,
    )  # user last time clicked
    time_multiplier: int = db.Column(
        db.Integer, default=1, server_default="1", nullable=False
    )  # user time multiplier

    def add_xp(self, amount: float) -> None:  # add XP
        """
        Add XP (experience points) to the user.
        amount - the amount to add XP.
        """
        current_time: datetime = datetime.utcnow()  # get current time
        time_difference: timedelta = (
            current_time - self.last_time_clicked
        )  # get time difference
        time_difference_seconds: float = (
            time_difference.total_seconds()
        )  # get time difference in seconds
        if (
            time_difference_seconds < 5
        ):  # check if time difference is less than 5 seconds
            self.time_multiplier += 1  # increase time multiplier
        else:
            self.time_multiplier = (
                1  # reset time multiplier if time difference is more than 5 seconds
            )
        self.last_time_clicked = current_time  # set last time clicked to current time
        if (
            amount == self.last_item_clicked
        ):  # check if amount is the same as last item clicked
            self.multiplier += 1  # increase multiplier
        else:
            self.multiplier = (
                1  # reset multiplier if amount is not the same as last item clicked
            )
        self.last_item_clicked = amount  # set last item clicked to amount
        self.xp += amount * self.multiplier * self.time_multiplier  # add XP by amount
        self.total_xp += (
            amount * self.multiplier * self.time_multiplier
        )  # add total XP by amount
        self.check_level_up()  # check if user has leveled up

    def check_level_up(self) -> None:  # check if user has leveled up
        """
        Check if the user has leveled up.
        """
        while (
            self.xp >= self.xp_required
        ):  # if user XP is greater than or equal to XP required
            self.xp -= self.xp_required
            self.xp_required = max(
                1.0,
                round(
                    self.xp_required
                    + max(1.0, self.xp_required * 1.0 / math.sqrt(self.level))
                ),
            )  # increase XP required exponentially with slower growth at higher levels
            self.level += 1  # increase level

    def get_xp_required(self) -> float:  # get required XP to next level
        """
        Get the required XP for the user to level up.
        """
        return self.xp_required

    def get_level_progress(self) -> float:  # get level progress
        """
        Get the level progress as a percentage.
        """
        return (self.xp / self.xp_required) * 100


@app.template_filter("short_numeric")  # short numeric filter
def short_numeric_filter(
    value: Union[int, float]
) -> str:  # get number in short numeric form with abbreviations
    """
    Get the abbreviated numeric value.
    value - the numeric value to convert.
    """
    units: list[str] = [
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
    mantissa: float = value  # mantissa value from 1 to 999
    while mantissa >= 1000:  # repeat until mantissa is within 1 to 999
        mantissa /= 1000
        exponent += 1
    return (
        f"{mantissa:.3g}{units[exponent]}" if value >= 1000 else f"{value:.0f}"
    )  # print abbreviated output


# add filter to Jinja
app.jinja_env.filters["short_numeric"] = short_numeric_filter


@app.route("/")  # index page
def index() -> str:  # get index page template
    """
    Return the index page containing a user.
    """
    user: Union[User, None] = User.query.first()  # get first user
    # redirect to index page template
    return render_template("index.html", user=user)


@app.route("/add_xp", methods=["POST"])  # add XP from POST method
def add_xp() -> Response:  # add XP
    """
    Add XP (experience points) based on entered amount.
    """
    user: Union[User, None] = User.query.first()  # get first user
    if user is not None:  # if user exists
        user.add_xp(float(request.form["amount"]))  # parse amount as float
    db.session.commit()  # commit database changes
    return redirect(url_for("index"))  # redirect to index page template


def init_db() -> None:  # initialize database
    """
    Initialize the user database.
    """
    with app.app_context():
        db.create_all()  # create tables if they don't exist
        if User.query.count() == 0:  # if there is no user in the database
            new_user = User(username="Player")  # add user with name 'Player'
            db.session.add(new_user)  # add new user to the database
            db.session.commit()  # commit database changes


if __name__ == "__main__":
    init_db()  # initialize database
    app.run(debug=True, port=8081)  # run the app at port 8081
