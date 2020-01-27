from ecommerce import app,db
from flask import request , jsonify, session
import secrets
from ecommerce.forms import *
from ecommerce.models import *
import os
import json
from PIL import Image
from ecommerce.functions import *


def supplier_product_data(pid):
    #products = db.session.query(Product , db.func.count(Order.id) , db.func.sum(Order.qty) , db.func.sum(Order.total_price), db.func.count(Reviews.id) , db.func.avg(Reviews.stars) ).filter(Product.supplier_id == supplier_id).outerjoin(Order).outerjoin(Reviews).group_by(Product).all()
    product = get_dict(db.session.query(Product).filter(Product.id == pid).first())
    product['order_count'], product['units_count'], product['review_count'], product['avg_rank'] = db.session.query(db.func.count(Order.id),db.func.sum(Order.qty),db.func.count(Reviews.id), db.func.avg(Reviews.stars)  ).outerjoin(Product).outerjoin(Reviews).filter(Order.product_id == pid).first()
    _, product['total_revenue'] = db.session.query(db.func.count(Order.id), db.func.sum(Order.total_price) ).filter(Order.product_id == pid).first()
    product['category'] = Category.query.get(product['the_category']).name
    product['open_order_count'] , product['open_order_units'], product['open_revenue'] = db.session.query(db.func.count(Order.id) , db.func.sum(Order.qty), db.func.sum(Order.total_price)).filter(Order.product_id == pid).filter(Order.status =="open").first()
    product['orders'] = get_dict(db.session.query(Order).filter(Order.product_id == pid).all())
    product['reviews'] = get_dict(db.session.query(Reviews).join(Order).filter(Order.product_id == pid).all())

    dec_2_float(product)
    return product



def product_belong_supplier(pid , supplier_id):
    if not Product.query.get(pid) or not Product.query.get(pid).supplier_id == supplier_id :
        return False
    else :
        return True


def supplier_products(supplier_id):
    #products = db.session.query(Product , db.func.count(Order.id) , db.func.sum(Order.qty) , db.func.sum(Order.total_price), db.func.count(Reviews.id) , db.func.avg(Reviews.stars) ).filter(Product.supplier_id == supplier_id).outerjoin(Order).outerjoin(Reviews).group_by(Product).all()
    products = get_dict(db.session.query(Product).filter(Product.supplier_id == supplier_id).all())
    for product in products:
        product['order_count'], product['units_count'], product['review_count'], product['avg_rank'] = db.session.query(db.func.count(Order.id),db.func.sum(Order.qty),db.func.count(Reviews.id), db.func.avg(Reviews.stars)  ).outerjoin(Product).outerjoin(Reviews).filter(Order.product_id == product['id']).first()
        _, product['total_revenue'] = db.session.query(db.func.count(Order.id), db.func.sum(Order.total_price) ).filter(Order.product_id == product['id']).first()
        product['category'] = Category.query.get(product['the_category']).name
        product['open_order_count'] , product['open_order_units'], product['open_revenue'] = db.session.query(db.func.count(Order.id) , db.func.sum(Order.qty), db.func.sum(Order.total_price)).filter(Order.product_id == product['id']).filter(Order.status =="open").first()
        try :
            product['avg_rank'] = round( product['avg_rank'] , 2 )
        except:
            pass
    dec_2_float(products)
    return products


def add_product(supplier_add_product):
    if supplier_add_product.picture.data :
        picture_fn = save_product_picture(supplier_add_product.picture.data)
    else:
        picture_fn= 'default.png'

    supplier_id = session['supplier_id']
    new_product = Product (name=supplier_add_product.name.data , supplier_id=supplier_id , price=supplier_add_product.price.data , product_type=supplier_add_product.category.data, category=supplier_add_product.category.data ,  product_sub_type=supplier_add_product.product_sub_type.data ,desc=supplier_add_product.desc.data , brand=supplier_add_product.brand.data, picture=picture_fn, Additional_information=supplier_add_product.Additional_information.data )
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
        return { 'login_error': 'password is not correct'  }
    else :
        return { 'login_error': 'username does not exists' }

def sup_signup(sup_signupform):
    print ('sup_signup run');
    try:
        new_supplier = Supplier(sup_signupform.email.data , sup_signupform.username.data , sup_signupform.password.data , sup_signupform.name.data , sup_signupform.type_of.data , sup_signupform.address.data)
        db.session.add(new_supplier)
        db.session.commit()
        return { 'signup_complete' : 'signup_successful' };
    except:
        return  { 'signup_error': 'signup_failed' }

def check_sup_user_event(forms):
    if forms['sup_loginform'].supplier_login.data and forms['sup_loginform'].validate_on_submit():
        return check_sup_login(forms['sup_loginform'])

    if session.get('supplier_username', None) is not None:
        return True

    if forms['sup_signupform'].supplier_signup.data and forms['sup_signupform'].validate_on_submit():
        return sup_signup(forms['sup_signupform'])