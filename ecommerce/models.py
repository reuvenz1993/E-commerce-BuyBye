from ecommerce import db,login_manager, ma
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from ecommerce.functions import save_photo
#import pdb


@login_manager.user_loader
def load_user(user_id):
    return Buyer.query.get(user_id)


def convert_to_list(val):
    temp = list()
    temp.append(val)
    return temp

class Coupon(db.Model, UserMixin):
    __tablename__ = 'coupon'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), default='N/A')
    product = db.Column(db.Integer, db.ForeignKey('products.id') , nullable=False)
    discount_amount = db.Column(db.Numeric , nullable=False )
    qty = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    db.relationship('Order', backref='the_coupon', lazy='dynamic' )

class Cart_status(db.Model, UserMixin):
    __tablename__ = 'cart_status'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), default='N/A')
    timeout = db.Column(db.Integer)
    is_open = db.Column(db.Boolean)
    carts = db.relationship('Cart', backref='the_status', lazy='dynamic' )

class Order_status(db.Model, UserMixin):
    __tablename__ = 'order_status'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), default='N/A')
    timeout = db.Column(db.Integer)
    is_open = db.Column(db.Boolean)
    orders = db.relationship('Order', backref='the_status', lazy='dynamic' )

class Category(db.Model, UserMixin):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), default='N/A')
    photo = db.Column(db.String(64), default='default.jpg')
    products = db.relationship('Product', backref='the_category', lazy='dynamic')

    def __init__(self, name , photo='default.jpg' ):
        self.name = name
        self.photo = photo


class Cart(db.Model, UserMixin):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key = True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id') , nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id') , nullable=False)
    qty = db.Column(db.String(256), default=1 , nullable=False)
    status = db.Column(db.Integer, db.ForeignKey('cart_status.id') , nullable=False)
    add_time = db.Column(db.DateTime)
    order_time = db.Column(db.DateTime)
    cancal_time = db.Column(db.DateTime)
    buyer_message= db.Column(db.String(256))
    purchase_way = db.Column(db.String(256), default='via cart')
    order_id = db.relationship('Order', backref='cart_item' , uselist=False)

    def __init__(self , buyer_id , product_id ,qty , status=1 , buy_now=False , buyer_message=False ):
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.qty = qty
        self.status = status
        self.add_time = datetime.utcnow()
        if not buy_now :
            self.purchase_way = 'via cart'
        if buy_now :
            self.purchase_way = 'buy now'
            if buyer_message:
                self.buyer_message = buyer_message
            db.session.add(self)
            db.session.commit()
            self.stamp_ordered()


    @property
    def price(self):
        return round(self.cart_product.price, 1)

    @property
    def total(self):
        return round(self.cart_product.price * int(self.qty), 1)


    def add_buyer_message(self , buyer_message=False):
        if buyer_message :
            self.buyer_message = buyer_message
        else:
            print ('you called add_buyer_message function without a message ')
        db.session.commit()

    def stamp_ordered(self , buyer_message=False):
        if buyer_message :
            self.buyer_message = buyer_message
            db.session.commit()
        order = Order (cart_item=self)
        db.session.add(order)
        db.session.commit()
        print('stamp_ordered')
        print(self.id)
        print(self.__dict__)
        self.status = 2
        self.order_time = datetime.utcnow()
        db.session.commit()
        return order.id

    def cancal(self):
        try :
            self.status = 3
            self.cancal_time = datetime.utcnow()
            db.session.commit()
            return True
        except:
            return False


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
    cart = db.relationship('Cart', backref='cart_buyer', lazy='dynamic')
    join_time = db.Column(db.DateTime)
    last_change_time = db.Column(db.DateTime)
    
    def __init__(self, email, username , password , name='N/A', address='N/A' , photo='default.jpg' ):
        self.email = email.lower()
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.name = name.lower()
        self.address = address.lower()
        self.photo = "/static/img/buyers/" + photo
        self.join_time  = datetime.utcnow()

    def check_password(self,password):
        return check_password_hash(self.password_hash , password)

    def as_list(self):
        return [self.id ,self.email ,self.username,self.password_hash,self.name,self.address,self.photo,self.orders]

    @property
    def open_cart(self):
        return self.cart.join(Cart_status).filter(Cart_status.is_open == True).all()
    
    @property
    def open_cart_count(self):
        return self.cart.join(Cart_status).filter(Cart_status.is_open == True).count()
    
    @property
    def sorted_orders(self):
        return self.orders.order_by(Order.status).order_by(Order.order_time.desc())
    
    @property
    def open_cart_total_price(self):
        return sum(item.total for item in self.open_cart)
    
    def update_personal(self , name=False , address=False):
        if name:
            self.name = name
        if address :
            self.address = address
        db.session.commit()



    # returns all cart item with statis active.
    def get_cart(self):
        return self.cart.filter(Cart.status == 'active').all()
    
    def add_to_cart(self , pid , qty):
        if not Product.query.get(pid) :
            print ('not such product')
            return False
        try :
            cart_item = Cart(buyer_id = self.id , product_id = pid , qty=qty)
            db.session.add(cart_item)
            db.session.commit(cart_item)
            return True
        except Exception as e:
            db_session.rollback()
            db_session.flush()
            print('add_to_cart function error')
            print (e)
            return False

    def cancel_cary_item(self , cart_id ):
        if not Cart.query.get(cart_id) or not Cart.query.get(cart_id).buyer_id == self.id :
            print ('no such cart item or item cart do not belong to buyer')
            return False
        res = Cart.query.get(cart_id).cancal()
        return res

    def get_info(self):
        response = dict()
        response['id']

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
    join_time = db.Column(db.DateTime)
    last_change_time = db.Column(db.DateTime)
    
    def __init__(self, email, username , password , name='N/A' , type_of='N/A', address='N/A' , photo='default.jpg' ):
        self.email = email.lower()
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.name = name
        self.type_of = type_of.lower()
        self.address = address.lower()
        self.photo = "/static/img/suppliers/" +  photo
        self.join_time  = datetime.utcnow()

    def check_password(self,password):
        return check_password_hash(self.password_hash , password)
    
    def get_info(self):
        response = dict()
        response['id'] = self.id
        response['name'] = self.name
        response['type_of'] = self.type_of
        response['address'] = self.address
        response['photo'] = self.address
        response['supplier_avg_stars'] = self.get_supplier_reviews(avg=True)['avg']
        
        return response


    def update_photo(self,picture):
        picture_fn = save_photo(photo=picture, dir='suppliers')
        self.photo = "/static/img/suppliers/" + picture_fn
        db.session.commit()

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
    
    @property
    def review_avg(self):
        res = db.session.query(db.func.avg(Reviews.stars)).join(Order, Order.id == Reviews.order_id).filter(Order.supplier_id == self.id).all()[0][0]
        if res :
            return round (res,2)
        else :
            return False


class Product(db.Model, UserMixin):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable=False)
    desc = db.Column(db.String(1024), default='N/A')
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id') , nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id') )
    brand = db.Column(db.String(256), default='N/A')
    price = db.Column(db.Numeric , nullable=False )
    picture = db.Column(db.String(64), default='default.jpg')
    Additional_information = db.Column(db.String(1024), default='N/A')
    orders = db.relationship('Order', backref='product', lazy='dynamic')
    cart = db.relationship('Cart', backref='cart_product', lazy='dynamic')
    add_time = db.Column(db.DateTime)
    last_change_time = db.Column(db.DateTime)
    coupons = db.relationship('Coupon', backref='coupons', lazy='dynamic')

    def __init__(self, name, supplier_id, price , product_sub_type='N/A' , desc='N/A' , brand='N/A' , picture='default.jpg' , Additional_information='N/A', category=1 ):
        self.name = name
        self.supplier_id = supplier_id
        self.price = price
        self.category = category
        self.product_sub_type = product_sub_type.lower()
        self.desc = desc
        self.brand = brand
        self.picture = "/static/img/products/" + picture
        self.add_time  = datetime.utcnow()
        self.last_change_time = datetime.utcnow()


    def as_list(self):
        return [self.id ,self.name ,self.desc,self.supplier_id, self.brand, float(self.price), self.picture, self.Additional_information]


    def get_info(self):
        response = self.__dict__
        if response['_sa_instance_state'] :
            del response['_sa_instance_state']
        response['price'] = float ( response['price'] )
        response['orders'] = self.get_product_orders( get_product_orders=False , sum_orders=True , sum_units=True)

        return response


    # returns dict  [get_orders_info]=array of order objects , *[order_count]-num of orders , *[units_sold]=units_sold
    def get_product_orders(self , get_product_orders=True , count_orders=False , count_units=False):
        response = dict()
        if get_product_orders:
            response['get_product_orders'] = db.session.query(Order).join(Product, Product.id == Order.product_id).filter(Order.product_id == self.id).all()

        if count_orders:
            response['count_orders'] = db.session.query(Order).join(Product, Product.id == Order.product_id).filter(Order.product_id == self.id).count()

        if count_units:
            response['count_units'] = db.session.query(db.func.sum(Order.qty)).join(Product, Product.id == Order.product_id).filter(Order.product_id == self.id).all()[0][0]

        return response



    def get_review(self , get_review=True , avg=False , count=False):
        response = dict()
        if get_review:
            response['get_review'] = db.session.query(Reviews).join(Order, Order.id == Reviews.order_id ).filter(Order.product_id == self.id).all()

        if avg :
            response['avg'] = db.session.query(db.func.avg(Reviews.stars)).join(Order, Order.id == Reviews.order_id ).filter(Order.product_id == self.id).all()[0][0]

        if count :
            response['count'] = db.session.query(db.func.count(Reviews.id)).join(Order, Order.id == Reviews.order_id ).filter(Order.product_id == self.id).all()[0][0]

        return response

    def update_picture(self,picture):
        picture_fn = save_photo(photo=picture,dir='product')
        self.picture = "/static/img/products/" + picture_fn
        db.session.commit()
        
    @property
    def order_count(self):
        return db.session.query(Order).filter(Order.product_id == self.id).count()
    
    @property
    def open_order_count(self):
        return db.session.query(Order).join(Order_status).filter(Order.product_id == self.id).filter(Order_status.is_open == True).count()
    
    @property
    def units_sold(self):
        res = db.session.query(db.func.sum(Order.qty)).join(Order_status).filter(Order.product_id == self.id).first()[0]
        if res :
            return res
        else :
            return 0
    
    @property
    def open_units_sold(self):
        res = db.session.query(db.func.sum(Order.qty)).join(Order_status).filter(Order.product_id == self.id).filter(Order_status.is_open == True).first()[0]
        if res :
            return res
        else :
            return 0
    
    @property
    def review_avg(self):
        res = db.session.query(db.func.avg(Reviews.stars)).join(Order, Order.id == Reviews.order_id).filter(Order.product_id == self.id).all()[0][0]
        if res :
            return round (res,2)
        else :
            return False
    
    @property
    def review_count(self):
        res = db.session.query(Reviews).join(Order, Order.id == Reviews.order_id).filter(Order.product_id == self.id).count()
        if res :
            return res
        else :
            return False

    @property
    def reviews(self):
        res = db.session.query(Reviews).join(Order).filter(Order.product_id == self.id)
        if res :
            return res
        else:
            return False

    @property
    def revenue(self):
        res = db.session.query(db.func.sum(Order.total_price)).filter(Order.product_id == self.id).first()[0]
        if res :
            return round(res, 0) 
        else :
            return 0

    @property
    def open_revenue(self):
        res = db.session.query(db.func.sum(Order.total_price)).join(Order_status).filter(Order.product_id == self.id).filter(Order_status.is_open == True).first()[0]
        if res :
            return round(res, 0) 
        else :
            return 0



class Order(db.Model, UserMixin):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id') , nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id') , nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id') , nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.utcnow)
    shipment_time = db.Column(db.DateTime)
    fulfillment_time = db.Column(db.DateTime)
    last_change_time = db.Column(db.DateTime)
    qty = db.Column(db.Integer, nullable=False , default=1 )
    status = db.Column(db.Integer, db.ForeignKey('order_status.id') , nullable=False)
    tracking_number = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric , nullable=False )
    total_price = db.Column(db.Numeric , nullable=False )
    reviews = db.relationship('Reviews', backref='order', lazy='dynamic' )
    buyer_message = db.Column(db.String(512))
    cart_item_id = db.Column(db.Integer, db.ForeignKey('cart.id'), unique=True )
    coupon = db.Column(db.Integer, db.ForeignKey('coupon.id') )

    def __init__(self, product_id=None, buyer_id=None, qty=None , status=1  , cart_item=False):

        if not cart_item and not (product_id or buyer_id or qty):
            print('missing info')
            return False

        if cart_item:
            self.product_id = cart_item.product_id
            self.buyer_id = cart_item.buyer_id
            self.qty = cart_item.qty
            self.cart_item_id = cart_item.id
            self.status = 1
            if cart_item.buyer_message :
                self.buyer_message = cart_item.buyer_message

        else :
            self.product_id = product_id
            self.buyer_id = buyer_id
            self.qty = qty

        self.supplier_id = Supplier.query.get((Product.query.get(self.product_id).supplier_id)).id
        self.order_time = datetime.utcnow()
        self.last_change_time = datetime.utcnow()
        self.status = status
        self.unit_price = Product.query.get(self.product_id).price
        self.total_price = float(self.qty)  *  float (self.unit_price)


    def make_shipment(self, tracking_number):
        self.status = 2
        self.tracking_number = tracking_number
        self.shipment_time = datetime.utcnow()
        self.last_change_time = datetime.utcnow()
        db.session.commit()

    def finish_order(self):
        self.status = 3
        db.session.commit()


    def as_list(self):
        return [self.id ,self.product_id ,self.buyer_id,self.supplier_id,self.order_time,self.qty,self.status,self.unit_price,self.total_price,self.reviews]

    def get_order_review(self):
        review = Reviews.query.filter_by(order_id=self.id).first()
        return review

    def submit_review(self, stars, review_content=None, return_review_object=False):
        if not self.reviews.first() and self.status == 3:
            review = Reviews(order=self, stars=stars, review_content=review_content)
            db.session.add(review)
            db.session.commit()
            if return_review_object :
                return {'success': len(self.reviews.all()) == 1 , 'review':self.reviews.first() }
            else :
                return {'success': len(self.reviews.all()) == 1 , 'review':self.reviews.first().id }

        return False

    
    def confirm_supplied(self):
        self.status = 3
        self.fulfillment_time = datetime.utcnow()
        self.last_change_time = datetime.utcnow()
        db.session.commit()


class Reviews(db.Model, UserMixin):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id') , nullable=False)
    stars = db.Column(db.Integer , default=5)
    review_content = db.Column(db.String(512), default="N/A")
    review_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, order, stars=5 , review_content="N/A"):

        if order and (Reviews.query.filter(Reviews.order_id == order.id).count() == 0)  :
            self.order_id = order.id
            self.stars = stars
            self.review_time = datetime.utcnow()
            if review_content:
                self.review_content = review_content
            else:
                self.review_content = "N/A"
        else :
            return False
        

    def as_list(self):
        return [self.id ,self.order_id ,self.stars,self.review_content,self.review_time]
    
    def get_review_order(self):
        print (self._sa_instance_state)
        print('review id : ' + str( self.id ) )
        print(self.order_id)
        try :
            return Order.query.get(self.order_id)
        except:
            return self.order_id

    def get_review_buyer(self):
        order = self.get_review_order()
        if type(order) == int :
            buyer_id = db.session.query(Order.buyer_id).filter(Order.id == order).first()
            return Buyer.query.get(buyer_id)
        return order.get_order_buyer()

    def get_review_supplier(self):
        order = self.get_review_order()
        return order.get_order_supplier()
    
    def get_review_product(self):
        order = self.get_review_order()
        return order.get_order_product()


class Categoryschema(ma.ModelSchema):
    class Meta:
        model = Category

class Cartschema(ma.ModelSchema):
    class Meta:
        model = Cart

class Buyerschema(ma.ModelSchema):
    class Meta:
        model = Buyer
        
class SupplierSchema(ma.ModelSchema):
    class Meta:
        model = Supplier
        
class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product
        
class OrderSchema(ma.ModelSchema):
    class Meta:
        model = Order
        
class ReviewsSchema(ma.ModelSchema):
    class Meta:
        model = Reviews

category_schema = Categoryschema(many=True)
buyer_schema = Buyerschema(many=True)
supllier_schema = SupplierSchema(many=True)
order_schema = OrderSchema(many=True)
cart_schema = Cartschema(many=True)
product_schema = ProductSchema(many=True)
reviews_schema = ReviewsSchema(many=True)