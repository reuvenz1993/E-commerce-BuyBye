from ecommerce import app, db
from ecommerce.models import *
from sqlalchemy import func, or_
from flask_login import login_user, login_required, logout_user, current_user
from flask import  request , jsonify, session
import json
import os
from PIL import Image
import secrets
from decimal import Decimal
import decimal

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


def dec_2_float(x):
    if isinstance(x , Decimal):
        print (x)
        x = int (x)
    if isinstance(x , list):
        for index in range(len(x)) :
            if isinstance(x[index] , Decimal):
                x[index] = int (x[index])
            else: 
                dec_2_float(x[index])

    elif isinstance(x , dict) :
        for key , value in x.items() :
            if isinstance(x[key], Decimal):
                x[key] = int (value)
            else :
                dec_2_float(x[key])


# function to abstract the use of schema, it gets a list or single object of any type of model and return a clean dict repr
def get_dict(object_or_list):
    import ecommerce
    if type(object_or_list) is list :
        if len(object_or_list) > 0 :
            schema = get_schema(object_or_list[0] , many=True )
        else :
            return None
    else :
        schema = get_schema(object_or_list , many=False )
    
    res = schema.dump(object_or_list)
    dec_2_float(res)
    return res
    

# gets object 
def get_schema(model , many=True):
    import ecommerce
    schema_type = ""
    models = (ecommerce.models.Category ,ecommerce.models.Cart ,ecommerce.models.Buyer ,ecommerce.models.Supplier , ecommerce.models.Product , ecommerce.models.Order , ecommerce.models.Reviews)
    schemas = [category_schema ,cart_schema , buyer_schema , supllier_schema , product_schema, order_schema  , reviews_schema ]
    arg = model
    for idx, val in enumerate(models):
        #print (s)
        #print (type(s))
        if isinstance(arg , val ):
            #print ('True')
            #print (idx)
            #print (val)
            #print (schemas[idx])
            model = idx
            schema = schemas[idx]
            schema.many = many
            return schema