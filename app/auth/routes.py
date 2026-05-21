from .utilis import load_user, send_reset_email
from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, logout_user
from app.forms import RegistrationForm, LoginForm, ResetPasswordForm, ResetRequestForm
from app.models import User
from app.extensions import bcrypt, db


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data.lower()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        gender = form.gender.data

        user = User(username=username, email=email, password=hashed_password, gender=gender)
        db.session.add(user)
        db.session.commit()

        flash("Your account have been created", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/register.html", form=form)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash("Your have successfully logged in", "success")
            return redirect(url_for("main.dashboard"))
        
        flash("Invalid email or password", "danger")
    
    return render_template("auth/login.html", form=form)

@auth.route("/logout")
def logout():
    logout_user()
    flash("Your have logged out", "success")
    return redirect(url_for("main.home"))


@auth.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect("main.dashboard")
    
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("No account found with that email", "danger")
            return redirect(url_for("auth.reset_request"))
        
        send_reset_email(user)
        flash("A message was sent to your email with the reset password link", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_request.html", form=form, title="Reset Password")


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect("main.dashboard")
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.verify_reset_token(token)
        
        if not user:
            flash("Reset token is invalid or has expired", "danger")
            return redirect(url_for("auth.reset_request"))
        
        user.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        db.session.commit()
        flash("Password successfully changed", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form, title="Reset Password")
