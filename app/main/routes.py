from flask import Blueprint, render_template
from flask_login import login_required
from app.models import User

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template("main/home.html")

@main.route("/about")
def about():
    return render_template("main/about.html")

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html")

@main.route("/leaderboard")
@login_required
def leaderboard():
    users = User.query.order_by(User.completed_task.desc()).limit(10)
    return render_template("main/leaderboard.html", users=users)