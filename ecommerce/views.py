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

functions = {'remove' : remove_from_cart, 'buy_one': buy_one ,'buy_all': buy_all}


categories = ['Sports' , 'House' , 'Electronics' , 'Men Clothing', 'Women Clothing', 'Phone accessories', 'Phones' , 'Computer and office']

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    forms = Forms()
    handle_forms(forms)
    data = {**forms, 'focus_order' : request.args.get('focus_order') }
    if request.args.get('focus_order') and int(request.args.get('focus_order')) in (order.id for order in current_user.orders):
        data['focus_on'] = int(request.args.get('focus_order'))

    return render_template('account.html', **data )


@app.route('/', methods = ['GET', 'POST'])
def index():
    forms = Forms()
    handle_forms(forms)
    data = {**forms ,'categorys': Category.query.all()}

    return render_template('index.html', **data )

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    return redirect (url_for('index'))



@app.route('/my_cart', methods = ['GET', 'POST'])
@login_required
def my_cart():
    data = {}
    forms = Forms()
    if request.args.get('type') in functions :
        res = functions[request.args.get('type')](item_id=request.args.get('item_id'))
        data['action'] = {'success': res , 'type': request.args.get('type'),'item': Cart.query.get(request.args.get('item_id', False))}
    
    return render_template('my_cart.html' , **forms , **data)


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
    # params : pid=[], category_list=[],min_price, max_price, min_avg,
    # word="search products contains this word", as_json=False(set true to get json response)
    if request.method == 'POST' and request.json:
        keyword_args = request.json
        results = search(**keyword_args)
        return render_template('result_rows.html', results=results)

    keyword_args = dict(request.args)
    for key,value in keyword_args.items():
        if key != 'word':
            if type(value) is list :
                keyword_args[key] = int(value[0])
            if type(value) is str :
                keyword_args[key] = int(value)
        if key =='word' and type(value) is list :
            keyword_args[key] = str(value[0])


    results = search(**keyword_args) # proform search with params, if keyword_args is None - return all products

    categorys = Category.query.all()

    return render_template('results.html'  , results=results , categorys=categorys , **forms, **keyword_args )


@app.route('/product2/<pid>', methods = ['GET', 'POST'])
def product(pid):
    forms = Forms()
    product = Product.query.get(pid)
    handle_forms(forms)
    if not product :
        return redirect (url_for('index'))

    return render_template('product2.html', **forms , product=product )