from ecommerce import app, db
from flask import render_template, redirect, request, url_for, flash, abort , jsonify, session
from ecommerce.forms import *
from ecommerce.models import *
from ecommerce.supplier_functions import *
from ecommerce.buyer_functions import *
from ecommerce.functions import *


@app.route('/suppliers/sup_orders', methods = ['GET', 'POST'])
def sup_orders():
    data = {'orders':pull_supplier_orders(sid=session.get('supplier_id')),
            'product_list': supplier_products(session.get('supplier_id'))}
    
    if request.method == 'GET':
        kwargs = {}
        kwargs['sid'] = session.get('supplier_id')
        data['pid'] = request.args.get('pid',False)
        data['status'] = request.args.get('status',False)

    if request.method == 'POST':
        kwargs = request.json
        kwargs['sid'] = session.get('supplier_id')
        data = {'orders': pull_supplier_orders(**kwargs) }
        return render_template('/suppliers/order_items.html' , **data )

    return render_template('/suppliers/sup_orders.html' , **data )



@app.route('/suppliers/', methods = ['GET', 'POST'])
def suppliers_index():
    data = {'forms': sup_forms()}
    if check_sup_user_event(data['forms']) == True :
        return redirect(url_for('suppliers_main'))
    else:
        data['login_signup_message']  = check_sup_user_event(forms)

    return render_template('/suppliers/index.html' , **data )


@app.route('/suppliers/main', methods = ['GET', 'POST'])
def suppliers_main():
    if session.get('supplier_username', None) is None:
        return redirect(url_for('suppliers_index'))
    data = { 'sup_username' : session.get('supplier_username'),
            'forms': sup_forms()}

    return render_template('/suppliers/main.html' , **data)


@app.route('/suppliers/sup_product_data/<pid>', methods = ['GET', 'POST'])
def sup_product_data(pid):
    if session.get('supplier_username', None) is None:
        return redirect(url_for('suppliers_index'))
    data = {'sup_username' : session.get('supplier_username') ,
            'sup_id' : session.get('supplier_id'),
            'forms': sup_forms(),
            'categorys': category_list(short=True) }
    data['products'] = supplier_products(data['sup_id'])
    
    if not product_belong_supplier(pid , data['sup_id'] ):
        return redirect(url_for('sup_products'))
    
    data['product_data'] = supplier_product_data(pid)
    
    return render_template('/suppliers/sup_product_data.html' , **data)



@app.route('/suppliers/sup_products', methods = ['GET', 'POST'])
def sup_products():
    if session.get('supplier_username', None) is None:
        return redirect(url_for('suppliers_index'))

    data = { 'sup_username' : session.get('supplier_username') ,
            'sup_id' : session.get('supplier_id'),
            'forms': sup_forms()}
    data['products'] = supplier_products(data['sup_id'])

    if data['forms']['supplier_add_product'].add_product.data and data['forms']['supplier_add_product'].validate_on_submit():
        add_product(data['forms']['supplier_add_product'])
        data['new_product'] = True

    return render_template('/suppliers/sup_products.html' , **data)




@app.route('/suppliers/logout', methods = ['GET', 'POST'])
def suppliers_logout():
    session.pop('supplier_username')
    return redirect(url_for('suppliers_index'))