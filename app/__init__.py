from extensions import db, bcrypt, login_manger, migrate
from flask import Flask
from ..config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manger.init_app(db)

    return app
