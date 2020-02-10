
from ecommerce import app, db
from flask import render_template, redirect, request, url_for, flash, abort , jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from ecommerce.functions import *
from ecommerce.buyer_functions import *
from ecommerce.supplier_functions import update_product
import json


@app.route('/supplier_update_info', methods = ['GET', 'POST'])
def supplier_update_info():
    supplier = Supplier.query.get(session.get('supplier_id'))

    if 'file' in request.files:
        supplier.update_photo(request.files['file'])
        return jsonify ([True , 'supplier photo updated' , supplier.photo])

    if request.method == 'POST' and 'input' in request.json and 'value' in request.json:
        if request.json['input'] in ['name', 'email', 'address'] and request.json['value'] not in [None , ""]:
            supplier.__setattr__(request.json['input'], request.json['value'])
            db.session.commit()
            if supplier.__getattribute__(request.json['input']) == request.json['value']:
                return jsonify([True , f"{request.json['input']} was changed"])

    return jsonify(False)


@app.route('/supplier_update_product', methods = ['GET', 'POST'])
def supplier_update_product():
    product = Product.query.get(request.form['product_id'])
    if not product or product.supplier_id != session.get('supplier_id') :
        return False

    if 'file' in request.files:
        product.update_picture(picture=request.files['file'])
        return jsonify ([True ,product.picture ])

    if 'input' in request.form and 'value' in request.form :
        res = update_product(product, request.form['input'], request.form['value'])
        if res :
            return jsonify([True , f"{request.form['input']} was changed"])

    return jsonify(False)


@app.route('/account_actions', methods = ['GET', 'POST'])
@login_required
def account_actions():
    if request.args.get('type' , None ) == 'confirm' and request.args.get('id' , None ):
        order = Order.query.get(request.args.get('id'))
        if order.buyer_id == current_user.id :
            order.confirm_supplied()
            return jsonify (order.status == 3)

    if 'type' in request.json and request.json['type'] == 'personal' :
        kwargs = {'name': request.json.get('name'), 'address':  request.json.get('address')}
        current_user.update_personal(**kwargs)
        return jsonify('personal info changed')

    return jsonify ( False )


@app.route('/buy_now_or_cart', methods = ['GET', 'POST'])
@login_required
def buy_now_or_cart():
    func = {'buy': buy_now, 'cart': add_to_cart }
    buyer_id = current_user.id
    # pick buy now / add to cart args('type') and execute it with args
    if request.json.get('type') in func:
        res = func[request.json.get('type')](buyer_id = buyer_id, **request.json)
        return jsonify (res)
    else :
        return jsonify (False)







'''
@app.route('/get_user_data', methods = ['GET', 'POST'])
@login_required
def get_buyer_data():

    buyer = { 'id' : current_user.id , 'username' : current_user.username , 'photo' : current_user.photo , 'address' : current_user.address }
    return jsonify(buyer)
'''


'''
# return a list of lists, for every category list return is [Category.id , Category.name , Number of products in category]
@app.route('/get_categories', methods = ['GET', 'POST'])
def get_categories():

    categories_list = db.session.query(Category.id , Category.name , db.func.count(Product.id)).outerjoin(Product).group_by(Category).all()
    return jsonify(categories_list)
'''


'''
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
'''



'''
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