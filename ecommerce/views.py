from ecommerce import app, db
from flask import render_template, redirect, request, url_for, flash, abort , jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from ecommerce.forms import *
from ecommerce.models import *
import secrets
import os
import json
from sqlalchemy.sql import text
from PIL import Image
from sqlalchemy import or_
from ecommerce.models import *
from ecommerce.functions import *
from ecommerce.buyer_functions import *
from ecommerce.api import *
from ecommerce.supplier_functions import *
import ecommerce.supllier_views


categories = ['Sports' , 'House' , 'Electronics' , 'Men Clothing', 'Women Clothing', 'Phone accessories', 'Phones' , 'Computer and office']

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    forms = Forms()
    data = {}
    data['orders'] = pull_buyer_orders(current_user.id)
    print(forms['signup_form'].signup.data and forms['signup_form'].validate_on_submit())
    if forms['signup_form'].signup.data and forms['signup_form'].validate_on_submit():
        print(forms['signup_form'].signup.data and forms['signup_form'].validate_on_submit())
        print('gg')
        signup_status = signup_buyer(forms['signup_form'])
        print (signup_status)
    if forms['login_form'].login.data and forms['login_form'].validate_on_submit():
        check_login(forms['login_form'])
    if current_user.is_authenticated:
        data['buyer'] = { 'id' : current_user.id , 'username' : current_user.username , 'photo' : current_user.photo , 'address' : current_user.address  , 'name' : current_user.name }
    

    return render_template('account.html' , login_form = forms['login_form'] , signup_form=forms['signup_form'] , data=data )



def handle_forms(forms):
    if forms['login_form'].login.data and forms['login_form'].validate_on_submit():
        check_login(forms['login_form'])
    print(forms['signup_form'].signup.data and forms['signup_form'].validate_on_submit())
    if forms['signup_form'].signup.data and forms['signup_form'].validate_on_submit():
        print(forms['signup_form'].signup.data and forms['signup_form'].validate_on_submit())
        print('gg')
        signup_status = signup_buyer(forms['signup_form'])
        print (signup_status)


@app.route('/', methods = ['GET', 'POST'])
def index():
    forms = Forms()
    data = {'categorys': Category.query.all()}
    handle_forms(forms)
    
    if current_user.is_authenticated:
        data['buyer'] = { 'id' : current_user.id , 'username' : current_user.username , 'photo' : current_user.photo , 'address' : current_user.address  , 'name' : current_user.name }
    

    return render_template('index.html' , login_form = forms['login_form'] , signup_form=forms['signup_form'] , data=data , **data )

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect (url_for('index'))


@app.route('/my_cart', methods = ['GET', 'POST'])
@login_required
def my_cart():
    forms = Forms()
    data = dict()
    cart = pull_cart(current_user.id)
    if current_user.is_authenticated:
        data['buyer'] = { 'id' : current_user.id , 'username' : current_user.username , 'photo' : current_user.photo , 'address' : current_user.address , 'name' : current_user.name  }
    return render_template('my_cart.html' , cart=cart , data=data  , login_form = forms['login_form'] , signup_form=forms['signup_form'])


@app.route('/results', methods = ['GET', 'POST'])
def results():
    forms = Forms()
    data = {}
    handle_forms(forms)
    product_type = 'all'
    filters = {}
    filters['product_type'] = request.args.get('product_type')
    filters['product_sub_type'] = request.args.get('product_sub_type')
    filters['brand'] = request.args.get('brand')
    filters['supplier_id'] = request.args.get('supplier_id')
    if current_user.is_authenticated:
        data['buyer'] = { 'id' : current_user.id , 'username' : current_user.username , 'photo' : current_user.photo , 'address' : current_user.address , 'name' : current_user.name }


    for key , value in filters.items():
        if value is not None :
            product_type = value
    
    #products = get_products(filters)
    #product_list = []
    #for p in products:
    #    product_list.append( p.as_list() )
    product_list = get_relvent_results(product_type)
    return render_template('results.html' , product_list = product_list , login_form = forms['login_form'] , signup_form=forms['signup_form'] , data=data)



@app.route('/new_order', methods = ['GET', 'POST'])
def new_order():
    forms = Forms()
    keyword_args = dict()

    if request.method == 'GET':

        pid = int ( request.args.get('pid') )
        if not Product.query.get(pid):
            return 'product does not exists'

        product = get_product_extra_info(pid)
        if product is False :
            return redirect (url_for('index'))

        if request.args.get('qty'):
            product['request_qty'] = int ( request.args.get('qty') )


    '''
    product = get_product_extra_info()
    if product is False :
        return redirect (url_for('index'))
    '''

    return render_template('new_order.html' , product = product , login_form = forms['login_form'] )




@app.route('/product2/<pid>', methods = ['GET', 'POST'])
def product(pid):
    forms = Forms()
    productt = Product.query.get(pid)
    data = {}
    handle_forms(forms)
    #product = get_product_extra_info(int(pid))
    if product is False :
        return redirect (url_for('index'))
    
    if current_user.is_authenticated:
        data['buyer'] = { 'id' : current_user.id , 'username' : current_user.username , 'photo' : current_user.photo , 'address' : current_user.address , 'name' : current_user.name  }


    return render_template('product2.html' , data=data , product2 = product , login_form = forms['login_form'] , signup_form=forms['signup_form'] , product=productt )


'''
@app.route('/product', methods = ['GET', 'POST'])
def results_item():
    if request.args.get('category', False):
        pid = request.args.get('category')
        req_product = Product.query.filter_by(id = pid).one()
        product_data = req_product.as_list()
        product_order_ids = Order.query.filter_by(product_id = pid).all()
        order_list = []
        for order in product_order_ids:
            order_list.append( order.as_list()[0] )
        reviews = Reviews.query.filter_by(order_id = order_list).all()

        return render_template('product.html', product_data = product_data , reviews = reviews)

    print('fdgdfg')
    category = request.args.get('category')
    products = Product.query.all()
    product_list = []
    for p in products:
        product_list.append( p.as_list() )
    print (category)
    return render_template('results.html' , product_list = product_list)

'''



'''
@app.route('/', methods = ['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    loginform = LoginForm()
    signupform = SignupForm()
    error = []
    msg = ''
    if loginform.login.data and loginform.validate_on_submit():
        print ("login")
        logged_in_user = User.query.filter_by(username = loginform.username.data).first()
        if ( logged_in_user is not None and logged_in_user.check_password(loginform.password.data) ) :
            print (logged_in_user)
            to_remember = loginform.remember.data
            login_user(logged_in_user , remember = to_remember)
            return redirect(url_for('home'))
        else:
            error.append('Invalid username or password')
            return render_template('index.html' , loginform = loginform , signupform = signupform , error = error )

    if signupform.signup.data and signupform.validate_on_submit():
        print('signup')
        register_user = User(email = signupform.email.data, 
                    username = signupform.username.data, 
                    password = signupform.password.data)
        db.session.add(register_user)
        try:
            db.session.commit()
            msg = 'register complete'
        except:
            db.session.rollback()
            error.append('register failed')
            if not register_user.check_if_username_free() :
                error.append('username already exists')
            if not register_user.check_if_email_free() :
                error.append('email already exists')

    loginform.reset()
    signupform.reset()
    return render_template('index.html' , loginform = loginform , signupform = signupform , error = error , msg = msg )


@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    msg = []
    addpost_form = AddPost()
    if addpost_form.addpost.data:
        addpost(current_user.id , addpost_form.data['title'], addpost_form.data['content'])
        msg.append('Post added')
        print ('added a post')
        addpost_form.reset()

    
    
    return render_template('home.html' , addpost_form = addpost_form , msg = msg)

@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect (url_for('index'))


@app.route('/account' , methods = ['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(username = current_user.username).first_or_404()
    posts = Post.query.filter_by(user_id = current_user.id).all()
    email = user.email
    updateform = UpdateForm()
    addpost_form = AddPost()
    updatephoto_form = UpdatePhoto()
    updateform.email.data = user.email
    profile_pic = url_for('static', filename = 'profile_pics/' + user.photo )
    if updatephoto_form.photo.data :
        picture_file = save_picture(updatephoto_form.photo.data)
        user.photo = picture_file
        db.session.commit()
        return redirect(url_for('account'))
    return render_template('account.html', user = user, posts = posts , email = email , updateform = updateform , addpost_form = addpost_form , updatephoto_form = updatephoto_form , profile_pic = profile_pic)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics' , picture_fn )
    output_size = (125 , 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_fn

@app.route('/home2', methods = ['GET', 'POST'])
@login_required
def home2():
    return render_template('home2.html')


@app.route('/index2', methods = ['GET', 'POST'])
@login_required
def index2():
    return render_template('index2.html')


def addpost( userid , title , content):
    new_post = Post(userid , title, content)
    db.session.add(new_post)
    db.session.commit()

'''