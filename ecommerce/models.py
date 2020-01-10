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
    return User.query.get(user_id)

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

    def __repr__(self):
        return f'username : {self.username} , email : {self.email} , password : {self.password_hash} ,photo = {self.photo}  '

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

    def __repr__(self):
        return f'by user : {self.username} , post : {self.post}  '


class Buyer(db.Model, UserMixin):

    __tablename__ = 'buyers'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True , nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(256), default='N/A')
    address = db.Column(db.String(256), default='N/A')
    photo = db.Column(db.String(64), default='default.jpg')
    orders = db.relationship('Order', backref='the_buyer', lazy=True)
    
    def __init__(self, email, username , password , name='N/A', address='N/A' , photo='default.jpg' ):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password_hash , password)


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
    products = db.relationship('Product', backref='supplier', lazy=True)
    orders = db.relationship('Order', backref='supplier', lazy=True)
    
    def __init__(self, email, username , password , name='N/A' , type_of='N/A', address='N/A' , photo='default.jpg' ):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)


class Product(db.Model, UserMixin):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable=False)
    desc = db.Column(db.String(1024), default='N/A')
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id') , nullable=False)
    product_type = db.Column(db.String(256), default='N/A')
    product_sub_type = db.Column(db.String(256), default='N/A')
    brand = db.Column(db.String(256), default='N/A')
    price = db.Column(db.Numeric , nullable=False )
    picture = db.Column(db.String(64), default='default.jpg')
    Additional_information = db.Column(db.String(1024), default='N/A')
    orders = db.relationship('Order', backref='product', lazy=True)

    def __init__(self, name, supplier_id, price , product_type='N/A', product_sub_type='N/A' , desc='N/A' , brand='N/A' , picture='default.jpg' , Additional_information='N/A' ):
        self.name = name
        self.supplier_id = supplier_id
        self.price = price
        self.product_type = product_type
        self.product_sub_type = product_sub_type
        self.desc = desc
        self.brand = brand
        self.picture = picture


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
    reviews = db.relationship('Reviews', backref='order', lazy=True)
    
    def __init__(self, product_id, buyer_id, supplier_id, unit_price, qty=1 , status='open'):
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.supplier_id = supplier_id
        self.order_time = datetime.utcnow()
        self.qty = qty
        self.status = status
        self.unit_price = unit_price
        self.total_price = qty * unit_price
    
    
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
