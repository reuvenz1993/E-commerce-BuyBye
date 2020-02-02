
from ecommerce import app, db
from flask import render_template, redirect, request, url_for, flash, abort , jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from ecommerce.functions import *
from ecommerce.buyer_functions import *
import json


@app.route('/edit_product_pic', methods = ['GET', 'POST'])
def edit_product_pic():
    if request.files['file'] and request.form['pid'] and Product.query.get(request.form['pid']):
        try :
            picture_fn = save_photo(photo=request.files['file'],dir='product')
            product = Product.query.get(request.form['pid'])
            product.update_picture(picture=picture_fn)
            return jsonify ([True ,product.picture ])
        except :
            return jsonify(False)


@app.route('/supplier_update_info', methods = ['GET', 'POST'])
def supplier_update_info():
    supplier = Supplier.query.get(session.get('supplier_id'))
    if 'file' in request.files and request.files['file'] :
        picture_fn = save_photo(photo=request.files['file'],dir='suppliers')
        supplier.update_photo(picture_fn)
        db.session.commit()
        return jsonify ([True , 'supplier photo updated' , supplier.photo])


    if request.method == 'POST' and 'input' in request.json and 'value' in request.json and request.json['value'] !='':
        if request.json['input'] == 'name' :
            supplier.name = request.json['value']
            db.session.commit()
            return jsonify([True , 'name was changed'])
        
        if request.json['input'] == 'email' :
            supplier.email = request.json['value']
            db.session.commit()
            return jsonify([True , 'email was changed'])
        
        if request.json['input'] == 'address' :
            supplier.address = request.json['value']
            db.session.commit()
            return jsonify([True , 'address was changed'])

@app.route('/supplier_update_product', methods = ['GET', 'POST'])
def supplier_update_product():
    if 'product_id' not in request.json or 'input' not in request.json or 'value' not in request.json :
        return jsonify(False)
    if ( not Product.query.get(request.json['product_id'])
         or not Product.query.get(request.json['product_id']).supplier_id == session.get('supplier_id') 
         or request.json['value'] in [None , ""]):
        return jsonify(False)

    if request.json['input'] not in ['name', 'desc' , 'category' , 'brand' , 'price' , 'Additional_information', 'picture'] :
        return jsonify(False)

    product = Product.query.get(request.json['product_id'])

    if request.json['input'] == 'name':
        product.name = request.json['value']
        db.session.commit()
        return jsonify([True , 'name was changed'])
    
    if request.json['input'] == 'desc':
        product.desc = request.json['value']
        db.session.commit()
        return jsonify([True , 'desc was changed'])
    
    if request.json['input'] == 'brand':
        product.brand = request.json['value']
        db.session.commit()
        return jsonify([True , 'brand was changed'])
    
    if request.json['input'] == 'Additional_information':
        product.Additional_information = request.json['value']
        db.session.commit()
        return jsonify([True , 'brand was changed'])
    
    if request.json['input'] == 'price':
        try :
            product.price = int (request.json['value'])
            db.session.commit()
            return jsonify([True , 'brand was changed'])
        except :
            return jsonify (False)
    
    if request.json['input'] == 'category':
        try :
            product.category = int (request.json['value'])
            db.session.commit()
            return jsonify([True , 'brand was changed'])
        except :
            return jsonify (False)
        
    
    return jsonify (False)




@app.route('/account_actions', methods = ['GET', 'POST'])
@login_required
def account_actions():
    if request.args.get('type' , None ) == 'confirm' and request.args.get('id' , None ):
        order_id = request.args.get('id')
        if Order.query.get(order_id).buyer_id == current_user.id :
            Order.query.get(order_id).confirm_supplied()
            db.session.commit()
            if Order.query.get(order_id).status == 'closed':
                return jsonify( True )
        return jsonify ( False )

    if 'type' in request.json :
        kwargs = {}
        if request.json['type'] == 'personal':
            if 'name' in request.json :
                kwargs['name'] = request.json['name']
            if 'address' in request.json :
                kwargs['address'] = request.json['address']
            Buyer.query.get(current_user.id).update_personal(**kwargs)
            db.session.commit()
            return jsonify( 'personal info changed' )
        return jsonify ( False )


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