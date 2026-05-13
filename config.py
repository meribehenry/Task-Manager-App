import os

class Config:
    FLASK_DEBUG=os.environ.get("FLASK_DEBUG")
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///app.db")
    UPLOAD_FOLDER=os.environ.get("UPLOAD_FOLDER")
    MAX_CONTENT_LENGT=int(os.environ.get("MAX_CONTENT_LENGTH", (3 * 1024 * 1024)))