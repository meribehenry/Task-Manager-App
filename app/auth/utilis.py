from flask import url_for
from app.extensions import login_manager
from app.models import User
from app.extensions import mail
from flask_mail import Message

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def send_reset_email(user):
    token = user.get_reset_token()
    message = Message("Password Reset Request", sender="noreply@gmail.com", recipients=[user.email])
    message.body = f"""
Please click the link below to reset your password
Link: {url_for("auth.reset_password", token=token, _external=True)}

If you didn't request this, just ignore the message nothing would be changed.
"""
    mail.send(message)
