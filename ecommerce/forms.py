from flask_dance.utils import first
from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField, StringField, SubmitField, BooleanField ,TextAreaField,
                     ValidationError , DecimalField )
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileField
from ecommerce.models import User
from ecommerce import db


class SupplierAddProduct(FlaskForm):
    name = StringField('*name : ' , validators=[DataRequired() ])
    desc = StringField('*desc : ' , validators=[DataRequired()] )
    product_type = StringField('*catgory: ',validators=[DataRequired()] )
    product_sub_type = StringField('sub_catgory : ' )
    brand = StringField('brand : ' )
    price = DecimalField('*price : ' , validators=[NumberRange(min=0 , max=100000000)] )
    Additional_information = StringField('Additional information : ' )
    picture = FileField()
    add_product = SubmitField("Add Product")
    


class SupplierSignupForm(FlaskForm):
    email = StringField('Enter your email : ' , validators=[DataRequired() ,Email() ])
    username = StringField('Enter Username : ' , validators=[DataRequired()] )
    password = PasswordField('Enter Password: ',validators=[DataRequired()] )
    name = StringField('Enter your store name : ' , validators=[DataRequired()] )
    type_of = StringField('Enter your type_of : ' , validators=[DataRequired()] )
    address = StringField('Enter your address : ' , validators=[DataRequired()] )
    supplier_signup = SubmitField("Sign up")



class SupplierLoginForm(FlaskForm):
    username = StringField('Enter Username : ' , validators=[DataRequired()] )
    password = PasswordField('Enter Password: ', validators=[DataRequired()] )
    remember = BooleanField('Remember Me')
    supplier_login = SubmitField("Log in")

class SignupForm(FlaskForm):
    email = StringField('Enter your email : ' , validators=[DataRequired() ,Email() ])
    username = StringField('Enter Username : ' , validators=[DataRequired()] )
    password = PasswordField('Enter Password: ',validators=[DataRequired()] )
    signup = SubmitField("Sign up")


    def reset(self):
        self.email.data = ""
        self.username.data = ""
        self.password.data = ""

class LoginForm(FlaskForm):
    username = StringField('Enter Username : ' , validators=[DataRequired()] )
    password = PasswordField('Enter Password: ', validators=[DataRequired()] )
    remember = BooleanField('Remember Me')
    login = SubmitField("Log in")

    def reset(self):
        self.username.data = ""
        self.password.data = ""

class AddPost(FlaskForm):
    title = StringField('Enter Title' , validators=[DataRequired()])
    content = TextAreaField('Enter Username : ' , validators=[DataRequired()] )
    addpost = SubmitField("Add Post")
    
    def reset(self):
        self.title.data = ""
        self.content.data = ""

class UpdateForm(FlaskForm):
    email = StringField('Enter your email : ' , validators=[DataRequired() ,Email() ])
    password = PasswordField('Enter Password: ',validators=[DataRequired()] )
    update = SubmitField("update")
    
class UpdatePhoto(FlaskForm):
    photo = FileField()
    Upload = SubmitField("update")
    
    
class Buyer_Login(FlaskForm):
    username = StringField('Enter Username : ' , validators=[DataRequired()] )
    password = PasswordField('Enter Password: ', validators=[DataRequired()] )
    remember = BooleanField('Remember Me')
    login = SubmitField("Log in")
    
    def reset(self):
        self.username.data = ""
        self.password.data = ""
        


class Buyer_Signup(FlaskForm):
    email = StringField('Enter your email : ' , validators=[DataRequired() ,Email() ])
    username = StringField('Enter Username : ' , validators=[DataRequired()] )
    password = PasswordField('Enter Password: ',validators=[DataRequired()] )
    signup = SubmitField("Sign up")


    def reset(self):
        self.email.data = ""
        self.username.data = ""
        self.password.data = ""