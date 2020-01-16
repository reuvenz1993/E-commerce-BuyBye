from ecommerce import app, db
from flask import render_template, redirect, request, url_for, flash, abort , jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from ecommerce.forms import *
from ecommerce.models import *
import secrets
import os
import json
from sqlalchemy.sql import text
# from PIL import Image

categories = ['Sports' , 'House' , 'Electronics' , 'Men Clothing', 'Women Clothing', 'Phone accessories', 'Phones' , 'Computer and office']

def check_sup_login(sup_loginform):
    print ('check_sup_login run');
    supplier_logging = Supplier.query.filter_by(username = sup_loginform.username.data).first()
    if ( supplier_logging is not None and supplier_logging.check_password(sup_loginform.password.data) ) :
        session['supplier_username'] = sup_loginform.username.data
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

@app.route('/suppliers/', methods = ['GET', 'POST'])
def suppliers_index():
    messages = dict()
    if session.get('supplier_username', None) is not None:
        return redirect(url_for('suppliers_main'))
    sup_loginform = SupplierLoginForm()
    sup_signupform = SupplierSignupForm()
    if sup_loginform.supplier_login.data and sup_loginform.validate_on_submit():
        validate = check_sup_login(sup_loginform)
        if validate == True :
            return redirect(url_for('suppliers_main'))
        else:
            messages['connection_error'] = validate
    if sup_signupform.supplier_signup.data and sup_signupform.validate_on_submit():
        signup = sup_signup(sup_signupform)
        if signup != True :
            messages['signup_error'] = signup
    return render_template('/suppliers/index.html' , sup_loginform = sup_loginform , sup_signupform = sup_signupform , messages = messages)


@app.route('/suppliers/main', methods = ['GET', 'POST'])
def suppliers_main():
    if session.get('supplier_username', None) is None:
        return redirect(url_for('suppliers_index'))
    sup_username = session.get('supplier_username')
    return render_template('/suppliers/main.html' , sup_username = sup_username)


@app.route('/suppliers/sup_products', methods = ['GET', 'POST'])
def sup_products():
    if session.get('supplier_username', None) is None:
        return redirect(url_for('suppliers_index'))
    sup_username = session.get('supplier_username')
    supplier_add_product = SupplierAddProduct()
    return render_template('/suppliers/sup_products.html' , sup_username = sup_username , supplier_add_product=supplier_add_product)


@app.route('/suppliers/logout', methods = ['GET', 'POST'])
def suppliers_logout():
    session.pop('supplier_username')
    return redirect(url_for('suppliers_index'))


@app.route('/get_categories', methods = ['GET', 'POST'])
def get_categories():
    
    categories = ['Sports' , 'House' , 'Electronics' , 'Men Clothing', 'Women Clothing', 'Phone accessories', 'Phones' , 'Computer and office']
    categories_arr = [[0] * 2 for i in range(len(categories))]
    for i in range(len(categories)):
        categories_arr[i][0] = categories[i]
        categories_arr[i][1] = Product.query.filter(Product.product_type == categories[i].lower()).count()
    return jsonify(categories_arr)



@app.route('/', methods = ['GET', 'POST'])
def index():
    login_form = Buyer_Login()
    if login_form.login.data and login_form.validate_on_submit():
        check_login(login_form)

    return render_template('index.html' , login_form = login_form , )

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect (url_for('index'))

def check_login(login_form):
    buyer_logging = Buyer.query.filter_by(username = login_form.username.data).first()
    if ( buyer_logging is not None and buyer_logging.check_password(login_form.password.data) ) :
        to_remember = login_form.remember.data
        login_user(buyer_logging , remember = to_remember)
        print ('login scss')
        

@app.route('/results', methods = ['GET', 'POST'])
def results():
    login_form = Buyer_Login()
    product_type = 'all'
    filters = {}
    filters['product_type'] = request.args.get('product_type')
    filters['product_sub_type'] = request.args.get('product_sub_type')
    filters['brand'] = request.args.get('brand')
    filters['supplier_id'] = request.args.get('supplier_id')

    for key , value in filters.items():
        if value is not None :
            product_type = value
    
    #products = get_products(filters)
    #product_list = []
    #for p in products:
    #    product_list.append( p.as_list() )
    product_list = get_relvent_results(product_type)
    return render_template('results.html' , product_list = product_list , login_form = login_form)

@app.route('/product2/<pid>', methods = ['GET', 'POST'])
def product(pid):
    login_form = Buyer_Login()
    product_data = Product.query.filter_by(id = pid).first()
    if product_data is None :
        return redirect (url_for('index'))
    product_data = product_data.as_list()
    product_data.append(get_product_extra_info(product_data[0]))
    reviews = get_reviews(pid)
    return render_template('product2.html' , product_data = product_data , reviews = reviews , login_form = login_form )

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

    login_form = Buyer_Login()
    print('fdgdfg')
    category = request.args.get('category')
    products = Product.query.all()
    product_list = []
    for p in products:
        product_list.append( p.as_list() )
    print (category)
    return render_template('results.html' , product_list = product_list)
        


@app.route('/get_results', methods = ['GET', 'POST'])
def get_results():
    product_type = request.form['product_type'].lower()
    min_price = request.form['min_price']
    max_price = request.form['max_price']
    min_stars = request.form['min_stars']
    products = get_relvent_results(product_type , min_price , max_price , min_stars)
    return jsonify( products )


def get_reviews(pid):
    orders = Order.query.filter_by(product_id = pid).all()
    order_list = []
    reviews = []
    for order in orders:
        order_list.append( order.as_list() )
        reviews.append(order.as_list()[9][0].as_list())
    for review in reviews:
        review_order = Order.query.filter_by(id = review[1]).one()
        buyer = Buyer.query.filter_by(id = review_order.buyer_id).one()
        review.append(buyer.name)
    return reviews


def get_products(filters):
    products = Product.query
    
    for key , value in filters.items():
        if value is not None :
            temp = str(key+" == '"+value+"'")
            temp2 = str(key+" == "+value)
            temp3 = str(key+" == '"+value+"'")
            products = products.filter(temp)

    print('gfhfgh')
    products = products.all()
    return products
    

def get_relvent_results(product_type , min_price = 0 , max_price = 100000 , min_stars = 1):
    if product_type != 'all':
        temp = str(product_type)
        products = Product.query.filter(Product.product_type == temp)
    else:
        products = Product.query

    products = products.filter(Product.price > min_price , Product.price < max_price )
    products = products.all()
    product_list = []
    for p in products:
        product_list.append( p.as_list() )
    for prod in product_list:
        prod.append(get_product_extra_info(prod[0]))
    return product_list



def get_product_extra_info(pid):
    product = Product.query.filter_by(id = pid).first()
    if product == None:
        print('product number : ' + str(pid) + ' not exists')
        return False 
    
    order_count = product.orders.count()
    order_list = product.orders.all()
    stars = 0
    reviews = []
    for order in order_list:
        for review in order.reviews:
            reviews.append(review)
            stars += review.stars
    
    review_count = len(reviews) 
    if review_count > 0 :
        avg = stars / len(reviews)
    else :
        avg = 5

    supplier_name = product_supplier_name(pid)
    return { 'order_count' : order_count , 'review_count':review_count , 'avg_stars': avg , 'supplier_name':supplier_name }

def product_supplier_name(pid):
    product = Product.query.filter_by(id = pid).first()
    supplier = Supplier.query.filter_by(id = product.supplier_id).first()
    return supplier.name


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