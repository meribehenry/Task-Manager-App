import os

class Config:
    FLASK_DEBUG=os.environ.get("FLASK_DEBUG")
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///app.db")
    UPLOAD_FOLDER=os.environ.get("UPLOAD_FOLDER")
    MAX_CONTENT_LENGTH=int(os.environ.get("MAX_CONTENT_LENGTH", (3 * 1024 * 1024)))
    MAIL_SERVER =os.environ.get("MAIL_SERVER")
    MAIL_PORT=int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS=os.environ.get("MAIL_USE_TLS", "False").lower() in ["true", "1", "t"]
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")