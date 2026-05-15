from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image
import secrets
import os

def save_picture(picture):
    filename = secure_filename(picture.filename)
    _, file_ext = os.path.splitext(filename)
    random_hex = secrets.token_hex(8)
    picture_name = random_hex + file_ext
    picture_path = os.path.join(current_app.config["UPLOAD_FOLDER"] + f'/{picture_name}')

    output_size = (100, 100)
    resized_picture = Image.open(picture)
    resized_picture.thumbnail(output_size)
    resized_picture.save(picture_path)

    return picture_name


