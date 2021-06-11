from ecommerce import app
import os
import secrets
from PIL import Image


file_locations = {
    "product": "../static/img/products",
    "buyer_photo": "../static/img/buyers",
    "suppliers": "../static/img/suppliers",
}


def save_photo(photo, _dir):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(photo.filename)
    photo_fn = random_hex + f_ext
    photo_path = os.path.join(app.root_path, file_locations[_dir], photo_fn)
    output_size = (800, 800)
    image = Image.open(photo)
    image.thumbnail(output_size)

    image.save(photo_path)
    return photo_fn
