from ecommerce import app,db
from flask import request , jsonify, session
import secrets
from ecommerce.forms import *
from ecommerce.models import *
import os
import json
from PIL import Image
from ecommerce.functions import *





def add_product(supplier_add_product):
    if supplier_add_product.picture.data :
        picture_fn = save_product_picture(supplier_add_product.picture.data)
    else:
        picture_fn= 'default.png'

    supplier_id = session['supplier_id']
    new_product = Product (name=supplier_add_product.name.data , supplier_id=supplier_id , price=supplier_add_product.price.data , product_type=supplier_add_product.product_type.data, product_sub_type=supplier_add_product.product_sub_type.data ,desc=supplier_add_product.desc.data , brand=supplier_add_product.brand.data, picture=picture_fn, Additional_information=supplier_add_product.Additional_information.data )
    db.session.add(new_product)
    db.session.commit()



def save_product_picture(picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/products' , picture_fn )
    output_size = (800 , 800)
    image = Image.open(picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_fn





def check_sup_login(sup_loginform):
    print ('check_sup_login run');
    supplier_logging = Supplier.query.filter_by(username = sup_loginform.username.data).first()
    if ( supplier_logging is not None and supplier_logging.check_password(sup_loginform.password.data) ) :
        session['supplier_username'] = sup_loginform.username.data
        session['supplier_id'] = Supplier.query.filter_by(username = sup_loginform.username.data).first().id
        return True
    elif supplier_logging is not None :
        return 'password is not correct'
    else :
        return 'username does not exists'

def sup_signup(sup_signupform):
    print ('sup_signup run');
    try:
        new_supplier = Supplier(sup_signupform.email.data , sup_signupform.username.data , sup_signupform.password.data , sup_signupform.name.data , sup_signupform.type_of.data , sup_signupform.address.data)
        db.session.add(new_supplier)
        db.session.commit()
        return True;
    except:
        return 'signup failed';