import os
from flask import render_template, redirect, request, url_for , jsonify
from flask_login import login_required, logout_user, current_user
from ecommerce import app
from ecommerce.forms import Forms
from ecommerce.models import *
from ecommerce.buyer_functions import handle_forms, update_buyer_message, remove_from_cart, buy_all, buy_one, search, authenticate_buyer_Oauth
from ecommerce.utils.GoogleAuth import GoogleStrategy, FacebookStrategy

PER_PAGE = 20

facebookKeys = {'scope': 'email', 
                'client_id': '265235621140167', 
                'redirect_uri': 'http://localhost:5000/auth/facebook/callback'}

GoogleKeys = {  'scope': 'profile+email',
                'access_type': 'offline',
                'redirect_uri' : 'http://localhost:5000/auth/google/callback',
                'client_id' : '1064746606031-kftok01lmpn0rsirm3l036lqr75pp20l.apps.googleusercontent.com'}


is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    facebookKeys['client_secret'] = os.environ.get('FACEBOOK_OUATH_SECRET', None)
    facebookKeys['redirect_uri']= 'https://reuven-flask-test.herokuapp.com/auth/facebook/callback'
    GoogleKeys['client_secret'] = os.environ.get('GOOGLE_OUATH_SECRET', None)
    GoogleKeys['redirect_uri']= 'https://reuven-flask-test.herokuapp.com/auth/facebook/callback'
else:
    from ecommerce.dev import facebook_oauth_secret, google_oauth_secret
    facebookKeys['client_secret'] = facebook_oauth_secret
    GoogleKeys['client_secret'] = google_oauth_secret

GoogleAuth = GoogleStrategy(**GoogleKeys)
FacebookAuth = FacebookStrategy(**facebookKeys)


@app.route('/auth/google', methods=['GET', 'POST'])
def google_login():
    return redirect(GoogleAuth.authenticationLink())


@app.route('/auth/google/callback', methods=['GET', 'POST'])
def google_completeAuth():
    authorizationCode = request.args.get('code')
    profile = GoogleAuth.completeAuth(authorizationCode)
    buyer = authenticate_buyer_Oauth(profile)
    
    return redirect(url_for('index'))


@app.route('/auth/facebook', methods=['GET', 'POST'])
def facebook_login():
    return redirect(FacebookAuth.authenticationLink())


@app.route('/auth/facebook/callback', methods=['GET', 'POST'])
def facebook_completeAuth():
    authorizationCode = request.args.get('code')
    profile = FacebookAuth.completeAuth(authorizationCode)
    buyer = authenticate_buyer_Oauth(profile)
    
    return redirect(url_for('index'))


@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        if 'page' in request.json:
            page = int(request.json.get('page', 1))
            orders = current_user.sorted_orders.paginate(page, PER_PAGE, False)
            return render_template('order_rows.html', orders = orders)

        elif 'stars' in request.json and 'order_id' in request.json:
            order = Order.query.get(int(request.json.get('order_id', 0)))
            del request.json['order_id']
            if order.id in (order.id for order in current_user.orders if not order.reviews.first()):
                return jsonify(order.submit_review(**request.json))
        else:
            return jsonify (False)

    forms = Forms()
    handle_forms(forms)
    data = {**forms, 'focus_order' : request.args.get('focus_order') }
    if request.args.get('focus_order') and int(request.args.get('focus_order')) in (order.id for order in current_user.orders):
        data['focus_on'] = int(request.args.get('focus_order'))

    data['orders'] = current_user.sorted_orders.paginate(1, PER_PAGE, False)

    return render_template('account.html', **data )


@app.route('/', methods = ['GET', 'POST'])
def index():
    forms = Forms()
    data = {**forms , 'categorys': Category.query.all()}
    user_messages = handle_forms(forms)
    if user_messages :
        data.update(user_messages)


    return render_template('index.html', **data )

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect (url_for('index'))


@app.route('/my_cart', methods = ['GET', 'POST'])
@login_required
def my_cart():
    forms = Forms()
    data = {**forms}
    args = request.args
    if args.get('type') == 'update_buyer_message':
        return jsonify(update_buyer_message(item_id = args.get('item_id'), buyer_message = args.get('buyer_message')))

    cart_functions = {'remove' : remove_from_cart, 'buy_one': buy_one , 'buy_all': buy_all}
    if args.get('type') in cart_functions:
        res = cart_functions[args.get('type')](item_id = args.get('item_id'))
        data['action'] = {'success': res, 'type': args.get('type'), 'item': Cart.query.get(args.get('item_id', False))}

    return render_template('my_cart.html', **data)


@app.route('/results', methods = ['GET', 'POST'])
def results():
    '''
    POST - render result_rows sub template
    if params on GET - return full template with relvent results
    else return template with all products
    '''
    forms = Forms()
    handle_forms(forms)
    
    # return result_rows sub template with the products in search results
    # params : pid = [], category_list = [], min_price, max_price, min_avg, 
    # word = "search products contains this word", as_json = False(set true to get json response)
    if request.method == 'POST' and request.json:
        keyword_args = request.json
        page = int(keyword_args.pop("page", 1))
        results = search(**keyword_args).paginate(page, PER_PAGE, False)

        return render_template('result_rows.html', results = results)

    keyword_args = dict(request.args)
    keyword_args.pop("page", None)
    for key, value in keyword_args.items():
        if key != 'word':
            if type(value) is list :
                keyword_args[key] = int(value[0])
            if type(value) is str :
                keyword_args[key] = int(value)
        if key == 'word' and type(value) is list :
            keyword_args[key] = str(value[0])


    results = search(**keyword_args).paginate(1, PER_PAGE, False)# proform search with params, if keyword_args is None - return all products

    categorys = Category.query.all()

    return render_template('results.html'  , results = results , categorys = categorys , **forms, **keyword_args )


@app.route('/product2/<pid>', methods = ['GET', 'POST'])
def product(pid):
    forms = Forms()
    handle_forms(forms)
    product = Product.query.get(pid)
    reviews = product.reviews
    if request.method == 'POST' and request.json and 'page' in request.json:
        page = int(request.json.get('page', 1))
        reviews = reviews.paginate(page, PER_PAGE, False)
        return render_template('product.html', product = product, reviews = reviews)
    
    reviews = reviews.paginate(1, PER_PAGE, False)
    data = {**forms, 'product': product, 'reviews': reviews}

    if not product :
        return redirect (url_for('index'))

    return render_template('product2.html', **data)