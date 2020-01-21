
from ecommerce import app, db
from flask import render_template, redirect, request, url_for, flash, abort , jsonify, session
from ecommerce.functions import *
import json



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