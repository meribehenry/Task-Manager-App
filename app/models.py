from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from app.extensions import db
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    profile_pic_id = db.Column(db.String(100), default="default", nullable=False)
    profile_pic_url = db.Column(
                                db.String(255), 
                                default="https://res.cloudinary.com/ddzmfmexs/image/upload/v1779357666/default_bqkr3f.jpg", 
                                nullable=False)
    completed_task = db.Column(db.Integer, default=0, nullable=False)
    tasks = db.relationship("Task", backref="user", lazy=True)

    def __repr__(self):
        return f"""
        Username: {self.username}
        Email: {self.email}
        Gender: {self.gender}
        """
    
    def get_reset_token(self):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id, "password_hash": self.password})
    
    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token, max_age=max_age)["user_id"]
            user_id = data["user_id"]
            password_hash = data["password_hash"]
        
        except (BadSignature, SignatureExpired):
            return None
        
        user = User.query.get(user_id)
        if user.password != password_hash:
            return None
        
        return user
        

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"""
        Task ID: {self.id}
        Date Added: {self.date_added}
        Deadline: {self.deadline}
        Status: {'Completed' if {self.is_completed} else 'Pending'}
        """
