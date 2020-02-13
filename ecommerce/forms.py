from flask_dance.utils import first
from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField, StringField, SubmitField, BooleanField ,TextAreaField,
                     ValidationError , DecimalField, SelectField )
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileField
from ecommerce.models import Category
from ecommerce import db


def Forms():
    forms = dict()
    forms['login_form'] = LoginForm()
    forms['signup_form'] = SignupForm()
    forms['updateform'] = UpdateForm()
    forms['sup_loginform'] = SupplierLoginForm()
    forms['sup_signupform'] = SupplierSignupForm()

    return forms

def sup_forms():
    forms = dict()
    forms['sup_loginform'] = SupplierLoginForm()
    forms['sup_signupform'] = SupplierSignupForm()
    forms['supplier_add_product'] = SupplierAddProduct()
    
    return forms
    



class SupplierAddProduct(FlaskForm):
    name = StringField('*name : ' , validators=[DataRequired() ])
    desc = TextAreaField('*desc : ' , validators=[DataRequired()] )
    category = SelectField('*catgory: ', coerce=int  , choices=db.session.query(Category.id , Category.name).all() )
    brand = StringField('brand : ' )
    price = DecimalField('*price : ' , validators=[NumberRange(min=0 , max=100000000)] )
    Additional_information = TextAreaField('Additional information : ' )
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
    email = StringField('Email : ' , validators=[DataRequired() ,Email() ])
    username = StringField('Username : ' , validators=[DataRequired()] )
    password = PasswordField('Password: ',validators=[DataRequired()] )
    name = StringField('Full name: ')
    address = StringField('Shipping Address : ' , validators=[DataRequired()] )
    photo = FileField()
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



class UpdateForm(FlaskForm):
    email = StringField('Enter your email : ' , validators=[DataRequired() ,Email() ])
    password = PasswordField('Enter Password: ',validators=[DataRequired()] )
    update = SubmitField("update")

'''
class UpdatePhoto(FlaskForm):
    photo = FileField()
    Upload = SubmitField("update")
    '''