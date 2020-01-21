from ecommerce import app, db
from flask import render_template, redirect, request, url_for, flash, abort , jsonify, session
from ecommerce.forms import *
from ecommerce.models import *
from ecommerce.supplier_functions import *
from ecommerce.buyer_functions import *



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
    messages =[]
    if session.get('supplier_username', None) is None:
        return redirect(url_for('suppliers_index'))
    sup_username = session.get('supplier_username')
    supplier_add_product = SupplierAddProduct()
    if supplier_add_product.add_product.data and supplier_add_product.validate_on_submit():
        add_product(supplier_add_product)
        messages.append('New Produce added !')
    return render_template('/suppliers/sup_products.html' , sup_username = sup_username , supplier_add_product=supplier_add_product ,messages=messages)




@app.route('/suppliers/logout', methods = ['GET', 'POST'])
def suppliers_logout():
    session.pop('supplier_username')
    return redirect(url_for('suppliers_index'))