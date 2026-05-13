from app.extensions import db, bcrypt, login_manager, migrate
from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    from .main.routes import main
    app.register_blueprint(main)
    
    from .auth.utilis import load_user

    return app
