from ecommerce import db
from flask import session
from ecommerce.models import *
from ecommerce.functions import save_photo

def update_product(product, field, value):
    if field not in ['name', 'desc' , 'category' , 'brand' , 'price' , 'Additional_information'] or value in [None , ""]:
        return False
    if field == 'price':
        value = float(value)
    if field == 'category':
        value = int(value)

    product.__setattr__(field, value)
    db.session.commit()
    return product.__getattribute__(field) == value


def pull_supplier_orders(sid , pid=False , status=False ):
    query = db.session.query(Order).filter(Order.supplier_id == sid)
    if pid :
        if type(pid) == int or  type(pid) == str:
            pid =  [int(pid)]
        query = query.filter(Order.product_id.in_(pid))

    if status :
        if type(status) == str:
            status =  [status]
        query = query.filter(Order.status.in_(status))

    return query.order_by(Order.status).order_by(Order.order_time.desc())


def product_belong_supplier(pid , supplier_id):
    if not Product.query.get(pid) or not Product.query.get(pid).supplier_id == supplier_id :
        return False
    else :
        return True


def add_product(supplier_add_product):
    if supplier_add_product.picture.data :
        picture_fn = save_photo(photo=supplier_add_product.picture.data, dir='product')
    else:
        picture_fn= 'default.png'

    supplier_id = session['supplier_id']
    new_product = Product (name=supplier_add_product.name.data, supplier_id=supplier_id,
                            price=supplier_add_product.price.data, category=supplier_add_product.category.data,
                            desc=supplier_add_product.desc.data , brand=supplier_add_product.brand.data,
                            picture=picture_fn, Additional_information=supplier_add_product.Additional_information.data )
    db.session.add(new_product)
    db.session.commit()

def check_sup_login(sup_loginform):
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
    try:
        new_supplier = Supplier(sup_signupform.email.data , sup_signupform.username.data , sup_signupform.password.data , sup_signupform.name.data , sup_signupform.type_of.data , sup_signupform.address.data)
        db.session.add(new_supplier)
        db.session.commit()
        return { 'signup_complete' : 'signup_successful' }
    except:
        return  { 'signup_error': 'signup_failed' }

def check_sup_user_event(forms):
    if forms['sup_loginform'].supplier_login.data and forms['sup_loginform'].validate_on_submit():
        return check_sup_login(forms['sup_loginform'])

    if session.get('supplier_username', None) is not None:
        return True

    if forms['sup_signupform'].supplier_signup.data and forms['sup_signupform'].validate_on_submit():
        return sup_signup(forms['sup_signupform'])