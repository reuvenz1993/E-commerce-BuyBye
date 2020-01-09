from flask_dance.utils import first
from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField, StringField, SubmitField, BooleanField ,TextAreaField,
                     ValidationError , FileField)
from wtforms.validators import DataRequired, Email, EqualTo
from blog.models import User
from blog import db


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