from datetime import datetime
from flask_login import UserMixin
from app.extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    profile_pic = db.Column(db.String(20), default="default_pic.jpg", nullable=False)
    completed_task = db.Column(db.Integer, default=0, nullable=False)
    tasks = db.relationship("Task", backref="user", lazy=True)

    def __repr__(self):
        return f"""
        Username: {self.username}
        Email: {self.email}
        Gender: {self.gender}
        """


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), unique=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    is_complete = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"""
        Username: {self.id}
        Date Added: {self.date_added}
        Deadline: {self.deadline}
        Status: {'Complete' if {self.is_complete} else 'Pending'}
        """
