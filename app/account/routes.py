from flask import Blueprint, flash, redirect, render_template, url_for, request
from app.forms import UpdateAccountForm
from flask_login import current_user, login_required
from app.models import User
from app.extensions import db
from .utilis import save_picture, delete_picture

account = Blueprint("account", __name__)


@account.route("/", methods=["GET", "POST"])
@login_required
def user_account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.profile_pic.data:
            profile_pic_url, profile_pic_id = save_picture(form.profile_pic.data)

            if current_user.profile_pic_id != "default":
                delete_picture(current_user.profile_pic_id)
                current_user.profile_pic_url, current_user.profile_pic_id = profile_pic_url, profile_pic_id

        if not form.profile_pic.data and current_user.username == form.username.data and current_user.email==form.email.data:
            return redirect(url_for("account.user_account"))
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account successfully updated", "success")
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