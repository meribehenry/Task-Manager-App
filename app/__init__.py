from app.extensions import db, bcrypt, login_manager, migrate
from flask import Flask
from config import Config
from app.extensions import mail
import cloudinary
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    mail.init_app(app)

    cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key = os.environ.get("CLOUDINARY_API_KEY"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET"),
    secure = True
)

    from .main.routes import main
    app.register_blueprint(main)
    from .auth.routes import auth
    app.register_blueprint(auth, url_prefix="/auth")
    from .task.routes import task
    app.register_blueprint(task, url_prefix="/task")
    from .account.routes import account
    app.register_blueprint(account, url_prefix="/account")
    from .errors.error_handlers import errors
    app.register_blueprint(errors, url_prefix="/error")

    return app
