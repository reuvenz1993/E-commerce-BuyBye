from ecommerce import *
from ecommerce.models import *
from ecommerce.forms import *
from sqlalchemy import func, or_
from flask_login import login_user, login_required, logout_user, current_user


def check_login(login_form):
    buyer_logging = Buyer.query.filter_by(username = login_form.username.data).first()
    if ( buyer_logging is not None and buyer_logging.check_password(login_form.password.data) ) :
        to_remember = login_form.remember.data
        login_user(buyer_logging , remember = to_remember)
        print ('login scss')



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

def search( pid = [x for x in range( Product.query.count()+1 )] ,min_price=0 , max_price=100000 , min_avg=0 , word=False ):
    
    if type(pid) == int :
        pid = [pid]


    search_query = db.session.query(Product.id).outerjoin(Order).outerjoin(Reviews).group_by(Product).having(or_(db.func.count(Reviews.id)==0 , db.func.avg(Reviews.stars) > min_avg )).subquery()


    #query = products.filter(Product.category.in_(pid))

    if word :
        word = "%{}%".format(word)
        search_query = Product.query.join(search_query , search_query.c.id == Product.id).filter(Product.name.like(word)).subquery()

    
    search_query = Product.query.join(search_query , search_query.c.id == Product.id).filter(Product.id.in_(pid) , Product.price > min_price , Product.price < max_price )

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
        row['avg_stars'] = product.get_review(avg=True)['avg']
        row['price'] = round( float( row['price'] ) , 1 )
        if row['_sa_instance_state']:
            del row['_sa_instance_state']
        products.append(row)
    
    return products
