from app.extensions import db, bcrypt, login_manager, migrate
from flask import Flask
from config import Config
from app.extensions import mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    mail.init_app(app)

    from .main.routes import main
    app.register_blueprint(main)
    from .auth.routes import auth
    app.register_blueprint(auth, url_prefix="/auth")
    from .task.routes import task
    app.register_blueprint(task, url_prefix="/task")
    from .account.routes import account
    app.register_blueprint(account, url_prefix="/account")

    return app
