
from ecommerce import app, db
from flask import render_template, redirect, request, url_for, flash, abort , jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from ecommerce.functions import *
from ecommerce.buyer_functions import *
import json


@app.route('/buy_now_or_cart', methods = ['GET', 'POST'])
@login_required
def buy_now_or_cart():
    keyword_args = {}
    keyword_args['buyer_id'] = current_user.id
    keyword_args['product_id'] = int( request.json['product_id'] )
    keyword_args['qty'] = int ( request.json['qty'] )

    #preform a buy now
    if request.json['type'] == 'buy':
        keyword_args['buy_now'] = True
        if 'buyer_message' in request.json :
            keyword_args['buyer_message'] = request.json['buyer_message']
        res = buy_now_or_add_to_cart(**keyword_args)

    #just add to cart
    if request.json['type'] == 'cart':
        res = buy_now_or_add_to_cart(**keyword_args)


    return jsonify (res)


@app.route('/cart_actions', methods = ['GET', 'POST'])
@login_required
def cart_actions():
    if request.args.get('type' , None ) == 'remove' and request.args.get('item_id' , None ) :
        item_id = request.args.get('item_id' , None )
        responce = remove_from_cart(cart_item_id=item_id)
        if responce:
            return redirect (url_for('my_cart'))
        else:
            print ('404')
            return abort(404)
    
    if request.args.get('type' , None ) == 'buy_one' and request.args.get('item_id' , None ) :
        item_id = request.args.get('item_id' , None )
        responce = buy_one(item_id)
        if responce:
            return redirect (url_for('my_cart'))
        else :
            return False
    
    if request.args.get('type' , None ) == 'buy_all':
        responce = buy_all(buyer_id = current_user.id)
        if responce :
            return redirect (url_for('my_cart'))
        return jsonify (str(responce))

        '''
        responce = { 'status':False , 'type' : request.json['type'] }
        item_id = request.json['cart_item']
        if not Cart.query.get(item_id) or not Cart.query.get(item_id).buyer_id == current_user.id:
            responce['message'] = 'no permission or item is not on cart'
            return jsonify (responce)
        Cart.query.get(item_id).cancal()
        if not Cart.query.get(item_id).status == 'canceled' :
            responce['message'] = 'cant confirm item was removed'
            return jsonify (responce)
        responce['status'] = True
        responce['message'] = 'item ' + item_id + 'removed'
        '''

    
    if request.json['type'] == 'buy_one':
        responce = { 'status':False , 'type' : request.json['type'] }
        kwargs = { item_id : request.json['type'] }
        item_id = request.json['cart_item']
        if 'buyer_message' in request.json :
            kwargs['buyer_message'] = request.json['buyer_message']
        order_id = buy_one(**kwargs)
        if order_id:
            responce['order_id'] = order_id
            responce['status'] = True

    if request.json['type'] == 'buy_all':
        pass

    return jsonify ( responce )


@app.route('/get_user_data', methods = ['GET', 'POST'])
@login_required
def get_buyer_data():

    buyer = { 'id' : current_user.id , 'username' : current_user.username , 'photo' : current_user.photo , 'address' : current_user.address }
    return jsonify(buyer)


# return a list of lists, for every category list return is [Category.id , Category.name , Number of products in category]
@app.route('/get_categories', methods = ['GET', 'POST'])
def get_categories():

    categories_list = db.session.query(Category.id , Category.name , db.func.count(Product.id)).outerjoin(Product).group_by(Category).all()
    return jsonify(categories_list)


@app.route('/get_search_res', methods = ['GET', 'POST'])
def get_search_res():

    if request.method == 'POST':

        keyword_args = request.json
        res = search(**keyword_args)
        return jsonify(res)

    if request.method == 'GET':
        keyword_args = dict()
        if request.args.get('min_price'):
            keyword_args['min_price'] = int ( request.args.get('min_price') )

        if request.args.get('max_price'):
            keyword_args['max_price'] = int ( request.args.get('max_price') )

        if request.args.get('min_avg'):
            keyword_args['min_avg'] = int ( request.args.get('min_avg') )

        if request.args.get('word'):
            keyword_args['word'] = request.args.get('word')
            
        if request.args.get('category_list'):
            keyword_args['category_list'] = request.args.get('category_list')
            
        category_list

        res = search(**keyword_args)
        return jsonify(res)

    return abort(404)



@app.route('/temp2/<pid>', methods = ['GET', 'POST'])
def get_product_data(pid):
    res = []
    responce = dict()
    
    product = Product.query.get(pid)
    responce = product.__dict__
    responce['price'] =  float( responce['price'] )
    responce['supplier'] = responce['supplier'].get_info()
    del responce['_sa_instance_state']
    #responce['product']['sum_orders'] = product.get_product_orders(sum_orders=True )['sum_orders']
    #responce['product']['sum_orders'] = product.get_product_orders( sum_units=True)['sum_units']
    print (responce)

    res.append(responce)
    return jsonify ( res )