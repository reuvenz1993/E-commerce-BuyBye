from ecommerce import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()

# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return Buyer.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True , nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    photo = db.Column(db.String(64), default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def check_if_username_free(self):
        if User.query.filter_by(username=self.username).first() is not None:
            return False
        else:
            return True

    def check_if_email_free(self):
        if User.query.filter_by(email=self.email).first() is not None:
            return False
        else:
            return True


    def update_photo(self,photo):
        self.photo = photo

        def update(self, email, username):
            self.email = email
            self.username = username


class Post(db.Model, UserMixin):
    # Create a table in the db
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(2048), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id') , nullable=False)

    def __init__(self, user_id, title , content):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.time = datetime.utcnow()


def convert_to_list(val):
    temp = list()
    temp.append(val)
    return temp



class Category(db.Model, UserMixin):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), default='N/A')
    product = db.relationship('Product', backref='category', lazy='dynamic')



class Buyer(db.Model, UserMixin):

    __tablename__ = 'buyers'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True , nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(256), default='N/A')
    address = db.Column(db.String(256), default='N/A')
    photo = db.Column(db.String(64), default='default.jpg')
    orders = db.relationship('Order', backref='the_buyer', lazy='dynamic')
    
    def __init__(self, email, username , password , name='N/A', address='N/A' , photo='default.jpg' ):
        self.email = email.lower()
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.name = name.lower()
        self.address = address.lower()
        self.photo = photo

    def check_password(self,password):
        return check_password_hash(self.password_hash , password)


    def as_list(self):
        return [self.id ,self.email ,self.username,self.password_hash,self.name,self.address,self.photo,self.orders]

    def get_orders(self):
        return self.orders.all()

    def get_reviews(self , count=False):
        response = dict()
        response['get_reviews'] = db.session.query(Reviews).join(Order , Reviews.order_id == Order.id ).filter(Order.buyer_id == self.id ).all()

        if count:
            response['count'] = db.session.query(Reviews).join(Order , Reviews.order_id == Order.id ).filter(Order.buyer_id == self.id ).count()

        return response

class Supplier(db.Model, UserMixin):

    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True , nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(256), default='N/A')
    type_of = db.Column(db.String(256), default='N/A')
    address = db.Column(db.String(256), default='N/A')
    photo = db.Column(db.String(64), default='default.jpg')
    products = db.relationship('Product', backref='supplier', lazy='dynamic')
    orders = db.relationship('Order', backref='supplier', lazy='dynamic')
    
    def __init__(self, email, username , password , name='N/A' , type_of='N/A', address='N/A' , photo='default.jpg' ):
        self.email = email.lower()
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.name = name
        self.type_of = type_of.lower()
        self.address = address.lower()
        self.photo = photo

    def check_password(self,password):
        return check_password_hash(self.password_hash , password)

    # gets an Supplier object and return list of his products
    def get_products(self):
        return self.products.all()

    #returns supplier orders , pramas = [1]status(list / string /int) , [2]pid(list / string /int), income=if True returns sum of revenue of supplier
    def get_orders(self , status=None , pid=None, count=False , income=False):
        response = dict()
        print (status)
        orders = Order.query.filter_by(supplier_id = self.id)
        if status :
            if type(status) is not list:
                status = convert_to_list(status)
            orders = orders.filter(Order.status.in_(tuple(status)))
        if pid :
            if type(pid) is not list:
                pid = convert_to_list(pid)
            orders = orders.filter(Order.product_id.in_(tuple(pid)))
        if count:
            response['count']= orders.count()
        if income:
            response['income'] = db.session.query(db.func.sum(Order.total_price)).join(Supplier, Order.supplier_id == Supplier.id ).filter(Order.supplier_id == self.id).all()[0][0]

        orders = orders.all()
        response['get_orders'] = orders
        
        
        return response

    def get_supplier_reviews(self , avg=False):
        response = dict()
        response['get_supplier_reviews']= db.session.query(Reviews).join(Order , Reviews.order_id == Order.id ).filter(Order.supplier_id == self.id ).all()

        if avg:
            response['avg'] = db.session.query(db.func.avg(Reviews.stars)).join(Order, Order.id == Reviews.order_id ).filter(Order.supplier_id == self.id).all()[0][0]

        return response


class Product(db.Model, UserMixin):

    __tablename__ = 'products'
    __searchable__ = ['name', 'desc']

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable=False)
    desc = db.Column(db.String(1024), default='N/A')
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id') , nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id') )
    product_type = db.Column(db.String(256), default='N/A')
    product_sub_type = db.Column(db.String(256), default='N/A')
    brand = db.Column(db.String(256), default='N/A')
    price = db.Column(db.Numeric , nullable=False )
    picture = db.Column(db.String(64), default='default.jpg')
    Additional_information = db.Column(db.String(1024), default='N/A')
    orders = db.relationship('Order', backref='product', lazy='dynamic')

    def __init__(self, name, supplier_id, price , product_type='N/A', product_sub_type='N/A' , desc='N/A' , brand='N/A' , picture='default.jpg' , Additional_information='N/A', category=1 ):
        self.name = name
        self.supplier_id = supplier_id
        self.price = price
        self.product_type = product_type.lower()
        self.category = category
        self.product_sub_type = product_sub_type.lower()
        self.desc = desc
        self.brand = brand
        self.picture = "/static/img/products/" + picture



    def as_list(self):
        return [self.id ,self.name ,self.desc,self.supplier_id,self.product_type,self.product_sub_type, self.brand, float(self.price), self.picture, self.Additional_information]

    # returns dict  [get_orders_info]=array of order objects , *[order_count]-num of orders , *[units_sold]=units_sold
    def get_product_orders(self , sum_orders=False , sum_units=False):
        response = dict()
        response['get_product_orders'] = db.session.query(Order).join(Product, Product.id == Order.product_id).filter(Order.product_id == self.id).all()
        #if res == []:
        # res = 'no reviews yet'
        if sum_orders:
            response['sum_orders'] = len(response['get_product_orders'])

        if sum_units:
            response['sum_units'] = db.session.query(db.func.sum(Order.qty)).join(Product, Product.id == Order.product_id).filter(Order.product_id == self.id).all()[0][0]

        return response



    def get_review(self , avg=False):
        response = dict()
        response['get_review'] = db.session.query(Reviews).join(Order, Order.id == Reviews.order_id ).filter(Order.product_id == self.id).all()

        if avg :
            response['avg'] = db.session.query(db.func.avg(Reviews.stars)).join(Order, Order.id == Reviews.order_id ).filter(Order.product_id == self.id).all()[0][0]

        return response
    
    

class Order(db.Model, UserMixin):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id') , nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id') , nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id') , nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.utcnow)
    qty = db.Column(db.Integer, nullable=False , default=1 )
    status = db.Column(db.String(256), default='open')
    unit_price = db.Column(db.Numeric , nullable=False )
    total_price = db.Column(db.Numeric , nullable=False )
    reviews = db.relationship('Reviews', backref='order', lazy='dynamic')

    def __init__(self, product_id, buyer_id, qty=1 , status='open'):
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.supplier_id = Supplier.query.get((Product.query.get(product_id).supplier_id)).id
        self.order_time = datetime.utcnow()
        self.qty = qty
        self.status = status
        self.unit_price = Product.query.get(product_id).price
        self.total_price = qty * self.unit_price


    def as_list(self):
        return [self.id ,self.product_id ,self.buyer_id,self.supplier_id,self.order_time,self.qty,self.status,self.unit_price,self.total_price,self.reviews]

    def get_order_review(self):
        review = Reviews.query.filter_by(order_id=self.id).first()
        return review

    def get_order_buyer(self):
        return Buyer.query.get(self.buyer_id)

    def get_order_supplier(self):
        return Supplier.query.get(Product.query.get(self.product_id).supplier_id)

    def get_order_product(self):
        return Product.query.filter_by(id=self.product_id).first()


class Reviews(db.Model, UserMixin):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id') , nullable=False)
    stars = db.Column(db.Integer , default=5)
    review_content = db.Column(db.String(512), default="N/A")
    review_time = db.Column(db.DateTime, default=datetime.utcnow)

    
    def __init__(self, order_id, stars=5 , review_content="N/A"):
        self.order_id = order_id
        self.stars = stars
        self.review_content = review_content
        self.review_time = datetime.utcnow()
        

    def as_list(self):
        return [self.id ,self.order_id ,self.stars,self.review_content,self.review_time]
    
    def get_review_order(self):
        return Order.query.filter_by(id=self.order_id).first()

    def get_review_buyer(self):
        order = self.get_review_order()
        return order.get_order_buyer()

    def get_review_supplier(self):
        order = self.get_review_order()
        return order.get_order_supplier()
    
    def get_review_product(self):
        order = self.get_review_order()
        return order.get_order_product()


