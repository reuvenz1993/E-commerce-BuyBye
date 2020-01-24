from ecommerce import app, db
from ecommerce.models import *
from sqlalchemy import func, or_
from flask_login import login_user, login_required, logout_user, current_user
from flask import  request , jsonify, session
import json
import os
from PIL import Image
import secrets

file_locations = { 'product':'static/img/products',
                  'buyer_photo':'static/img/buyers' }

def save_photo(photo , dir):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(photo.filename)
    photo_fn = random_hex + f_ext
    photo_path = os.path.join(app.root_path, file_locations[dir] , photo_fn )
    output_size = (800 , 800)
    image = Image.open(photo)
    image.thumbnail(output_size)
    image.save(photo_path)
    return photo_fn

