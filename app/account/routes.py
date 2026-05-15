from flask import Blueprint, flash, redirect, render_template, url_for, request
from app.forms import UpdateAccountForm
from flask_login import current_user, login_required
from app.models import User
from app.extensions import db
from .utilis import save_picture

account = Blueprint("account", __name__)


@account.route("/", methods=["GET", "POST"])
@login_required
def user_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            profile_pic = save_picture(form.profile_pic.data)
            current_user.profile_pic = profile_pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account successfully updated")
        return redirect(url_for("account.user_account"))
    
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template("account/user_account.html", form=form, title="User Account")

@account.route("/view/<int:user_id>")
@login_required
def view_account(user_id):
    user = User.query.get_or_404(int(user_id))
    return render_template("account/view_account.html", user=user, title="User Account")