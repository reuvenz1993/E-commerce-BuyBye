from ecommerce import *
from ecommerce.models import *
from ecommerce.forms import *
from sqlalchemy import func, or_
from flask_login import login_user, login_required, logout_user, current_user
from ecommerce.functions import *

def category_list():
    data = db.session.query(Category.id , Category.name , db.func.count(Product.id)).outerjoin(Product).group_by(Category).all()
    return data

def check_login(login_form):
    buyer_logging = Buyer.query.filter_by(username = login_form.username.data).first()
    if ( buyer_logging is not None and buyer_logging.check_password(login_form.password.data) ) :
        to_remember = login_form.remember.data
        login_user(buyer_logging , remember = to_remember)
        print ('login scss')



def pull_cart(buyer_id):
    cart = []
    for item in Buyer.query.get(buyer_id).get_cart():
        cart_item = item.__dict__
        if cart_item['_sa_instance_state']:
            del cart_item['_sa_instance_state']
        cart_item['unit_price'] = float( Product.query.get(item.product_id).price )
        cart_item['total'] = cart_item['unit_price'] * int(item.qty)
        cart_item['product']=get_product_extra_info(cart_item['product_id'])
        cart.append(cart_item)
    
    return { 'cart' : cart , 'cart_size': len(cart) }


@app.route('/get_results', methods = ['GET', 'POST'])
def get_results():
    product_type = request.form['product_type'].lower()
    min_price = request.form['min_price']
    max_price = request.form['max_price']
    min_stars = request.form['min_stars']
    products = get_relvent_results(product_type , min_price , max_price , min_stars)
    return jsonify( products )


def buy_now_or_add_to_cart(buyer_id , product_id , qty , buyer_message=False , buy_now=False ):
    if not Buyer.query.get(buyer_id) or not Product.query.get(product_id):
        print ('buyer or product not exist')
        return False

    if buy_now :
        kwargs = { 'buyer_id' : buyer_id , 'product_id' : product_id, 'qty' : qty , 'buy_now' : buy_now }
        if buyer_message :
            kwargs['buyer_message'] = buyer_message
        try :
            cart_item = Cart( **kwargs )
            db.session.add(cart_item)
            db.session.commit()
            order = Order(cart_item=cart_item)
            db.session.add(order)
            db.session.commit()
            print('inner :' + str( cart_item.id ))
            cart_item.stamp_ordered()
            db.session.commit()
            return { 'cart_item':cart_item.id , 'order':order.id}
        except Exception as e:
            print ('buy_now_or_add_to_cart function fail - on buy now action')
            print(e)
            return False
    
    else :
        kwargs = { 'buyer_id' : buyer_id , 'product_id' : product_id, 'qty' : qty }
        try :
            cart_item = Cart( **kwargs )
            db.session.add(cart_item)
            db.session.commit()
            return { 'cart_item':cart_item.id , 'cart_size': len(Buyer.query.get(buyer_id).get_cart()) }
        except Exception as e:
            print ('buy_now_or_add_to_cart function fail - onvia cart action')
            print(e)
            return False


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
    if not product :
        print('product number : ' + str(pid) + ' not exists')
        return False

    product_data = product.__dict__
    product_data['supplier'] = product.supplier.get_info()
    product_data['reviews'] = product.get_review(get_review=True ,avg=True , count=True)
    reviews = []
    for rev in product_data['reviews']['get_review']:
        temp = rev
        rev = temp.__dict__
        rev['reviewer'] = temp.get_review_buyer().name
        if rev['_sa_instance_state']:
            del rev['_sa_instance_state']
        reviews.append(rev)
    product_data['reviews']['get_review'] = reviews
    product_data['orders'] = product.get_product_orders( get_product_orders=False, count_orders=True , count_units=True)
    product_data['price'] = round( float( product_data['price'] ) , 1 )
    if product_data['_sa_instance_state']:
        del product_data['_sa_instance_state']

    return product_data


def product_supplier_name(pid):
    product = Product.query.filter_by(id = pid).first()
    supplier = Supplier.query.filter_by(id = product.supplier_id).first()
    return supplier.name

def search( pid = [i for i in range( Product.query.count()+1 )] , category_list = [i for i in range( Category.query.count()+1 )] ,min_price=0 , max_price=100000 , min_avg=0 , word=False ):
    
    if type(pid) == int :
        pid = [pid]
    
    if type(category_list) == int :
        category_list = [category_list]


    search_query = db.session.query(Product.id).outerjoin(Order).outerjoin(Reviews).group_by(Product).having(or_(db.func.count(Reviews.id)==0 , db.func.avg(Reviews.stars) > min_avg )).subquery()


    #query = products.filter(Product.category.in_(pid))

    if word :
        word = "%{}%".format(word)
        search_query = Product.query.join(search_query , search_query.c.id == Product.id).filter(Product.name.like(word)).subquery()

    
    search_query = Product.query.join(search_query , search_query.c.id == Product.id).filter(Product.id.in_(pid) , Product.category.in_(category_list) , Product.price > min_price , Product.price < max_price )

    #if min_price:
    #    products = products.filter(Product.price > min_price )

    #if max_price:
    #    products = products.filter(Product.price < max_price )

    #search_query = search_query.all()
    #temp = search_query.all()
    
    products = []
    for product in search_query :
        row = product.__dict__
        row['supplier'] = product.supplier.get_info()
        row['reviews'] = product.get_review(get_review=False ,avg=True , count=True)
        row['orders'] = product.get_product_orders( get_product_orders=False, count_orders=True , count_units=True)
        row['price'] = round( float( row['price'] ) , 1 )
        if row['_sa_instance_state']:
            del row['_sa_instance_state']
        products.append(row)
    
    return products
