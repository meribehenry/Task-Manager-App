from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image
import secrets
import os
import cloudinary.uploader


def save_picture(picture):
    picture_id = secrets.token_hex(16)

    result = cloudinary.uploader.upload(
        picture,
        public_id = picture_id,
        folder = "profile_pics",
        resource_type = "auto"      
    )

    return result["secure_url"], picture_id


def delete_picture(picture_id):
    cloudinary.uploader.destroy(picture_id, resource_type="image", invalidate=True)
