import os

class Config:
    FLASK_DEBUG=True
    SECRET_KEY=os.environ.get("SECRET_KEY")
    DATABASE_URL=os.environ.get("DATABASE_URL")
    UPLOAD_FOLDER=os.environ.get("UPLOAD_FOLDER")
    MAX_CONTENT_LENGT=os.environ.get("MAX_CONTENT_LENGTH")