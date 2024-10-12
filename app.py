"""
A simple Flask application for a user with level and XP (experience points) system.
"""

import math
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)


class User(db.Model):
    """
    A user model to store the level and experience points (XP).
    """

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    xp = db.Column(db.Float, default=0)
    xp_required = db.Column(db.Float, default=1)
    total_xp = db.Column(db.Float, default=0)
    level = db.Column(db.Integer, default=1)

    def add_xp(self, amount):
        """
        Add XP (experience points) to the user.
        """
        self.xp += amount
        self.total_xp += amount
        while self.xp >= self.xp_required:
            self.xp -= self.xp_required
            self.xp_required = round(
                self.xp_required + self.xp_required * 1 / math.sqrt(self.level)
            )
            self.level += 1

    def get_xp_required(self):
        """
        Get the required XP for the user to level up.
        """
        return self.xp_required

    def get_level_progress(self):
        """
        Get the level progress as a percentage.
        """
        return (self.xp / self.xp_required) * 100


@app.template_filter("short_numeric")
def short_numeric_filter(value):
    if value < 1000:
        return "{:.0f}".format(value)
    elif value < 1000000:
        return "{:.1f}K".format(value / 1000)
    elif value < 1000000000:
        return "{:.1f}M".format(value / 1000000)
    else:
        return "{:.1f}B".format(value / 1000000000)


app.jinja_env.filters["short_numeric"] = short_numeric_filter


@app.route("/")
def index():
    """
    Return the index page containing a user.
    """
    user = User.query.first()
    return render_template("index.html", user=user)


@app.route("/add_xp", methods=["POST"])
def add_xp():
    """
    Add XP (experience points) based on entered amount.
    """
    user = User.query.first()
    user.add_xp(float(request.form["amount"]))
    db.session.commit()
    return redirect(url_for("index"))


def init_db():
    """
    Initialize the user database.
    """
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            new_user = User(username="Player")
            db.session.add(new_user)
            db.session.commit()


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=8081)
