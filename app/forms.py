from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, PasswordField, RadioField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import Email, EqualTo, DataRequired, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", 
                            validators=[DataRequired(message="Please enter this field"), 
                            Length(min=2, max=20, message="Username must be within 2-20 characters long")])
    
    email = EmailField("Email", 
                       validators=[
                            DataRequired(message="Please enter this field"), 
                            Email(message="Please enter a valid email"), 
                            Length(max=100, message="Email cannot be more than 100 characters long")])
    
    password = PasswordField("Password", 
                            validators=[
                                DataRequired(message="Please enter this field"),
                                Length(min=5, message="Password must be atleast 5 characters long")])
    
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    gender = RadioField(choices=[("male", "Male"), ("female", "Female")], validators=[DataRequired()])

    submit = SubmitField("Sign Up")
    

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if not username.data.isalum():
            raise ValidationError(f"Username must contain letters and numbers")
        
        if not user:
            raise ValidationError(f"Username '{username.data}' already exists")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        
        if not user:
            raise ValidationError(f"Email '{email.data}' already exists")


class LoginForm(FlaskForm):
    email = EmailField("Email", 
                       validators=[
                            DataRequired(message="Please enter this field"), 
                            Email(message="Please enter a valid email"), 
                            Length(max=100, message="Email cannot be more than 100 characters long")])
    
    password = PasswordField("Password", 
                             validators=[
                                DataRequired(message="Please enter this field"),
                                Length(min=5, message="Password must be atleast 5 characters long")])

    remember = BooleanField("Remember Me")

    submit = SubmitField("Sign In")


class TaskForm(FlaskForm):
    task = StringField("Task", 
                        validators=[DataRequired(message="Please enter this field"), 
                        Length(max=500, message="Task cannot be more than 500 characters long")])
    
    deadline = DateTimeField("Deadline", 
                            validators=[DataRequired(message="Please enter this field")], 
                            format= "%Y-%m-%d %H:%M")
    
    submit = SubmitField("Add")


class MarkTaskForm(FlaskForm):
    complete = BooleanField()
    submit = SubmitField("Mark Complete")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", 
                            validators=[DataRequired(message="Please enter this field"), 
                            Length(min=2, max=20, message="Username must be within 2-20 characters long")])
    
    email = EmailField("Email", 
                        validators=[
                            DataRequired(message="Please enter this field"), 
                            Email(message="Please enter a valid email"), 
                            Length(max=100, message="Email cannot be more than 100 characters long")])
    
    profile_pic = FileField("Upload Image", validators=[FileAllowed(["png", "jpg", "jpeg", "img"])])


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if username.data != current_user.username:
            if not username.data.isalum():
                raise ValidationError(f"Username must contain only letters or numbers")
            
            if not user:
                raise ValidationError(f"Username '{username.data}' already exists")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        
        if email.data.lower() != current_user.email:
            if not user:
                raise ValidationError(f"Email '{email.data}' already exists")
