from ecommerce import app,db
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user, current_user
from ecommerce.forms import *
from ecommerce.models import User , Post
import secrets
import os
#from PIL import Image


@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = Buyer_Login()
    if login_form.login.data and login_form.validate_on_submit():
        check_login()

    return render_template('index.html' , login_form=login_form)

def check_login():
    buyer_logging = Buyer.filter_by(username=login_form.username.data).first()
    if ( buyer_logging is not None and buyer_logging.check_password(loginform.password.data) ) :
        to_remember = login_form.remember.data
        login_user(buyer_logging , remember = to_remember)
        print ('login scss')










'''
@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    loginform = LoginForm()
    signupform = SignupForm()
    error = []
    msg = ''
    if loginform.login.data and loginform.validate_on_submit():
        print ("login")
        logged_in_user = User.query.filter_by(username=loginform.username.data).first()
        if ( logged_in_user is not None and logged_in_user.check_password(loginform.password.data) ) :
            print (logged_in_user)
            to_remember = loginform.remember.data
            login_user(logged_in_user , remember = to_remember)
            return redirect(url_for('home'))
        else:
            error.append('Invalid username or password')
            return render_template('index.html' , loginform = loginform , signupform = signupform , error = error )

    if signupform.signup.data and signupform.validate_on_submit():
        print('signup')
        register_user = User(email=signupform.email.data,
                    username=signupform.username.data,
                    password=signupform.password.data)
        db.session.add(register_user)
        try:
            db.session.commit()
            msg = 'register complete'
        except:
            db.session.rollback()
            error.append('register failed')
            if not register_user.check_if_username_free() :
                error.append('username already exists')
            if not register_user.check_if_email_free() :
                error.append('email already exists')

    loginform.reset()
    signupform.reset()
    return render_template('index.html' , loginform = loginform , signupform = signupform , error = error , msg=msg )


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    msg = []
    addpost_form= AddPost()
    if addpost_form.addpost.data:
        addpost(current_user.id , addpost_form.data['title'], addpost_form.data['content'])
        msg.append('Post added')
        print ('added a post')
        addpost_form.reset()

    
    
    return render_template('home.html' , addpost_form=addpost_form , msg=msg)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect (url_for('index'))


@app.route('/account' , methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.filter_by(user_id=current_user.id).all()
    email = user.email
    updateform = UpdateForm()
    addpost_form= AddPost()
    updatephoto_form= UpdatePhoto()
    updateform.email.data = user.email
    profile_pic = url_for('static', filename='profile_pics/' + user.photo )
    if updatephoto_form.photo.data :
        picture_file = save_picture(updatephoto_form.photo.data)
        user.photo = picture_file
        db.session.commit()
        return redirect(url_for('account'))
    return render_template('account.html', user=user, posts=posts , email=email , updateform=updateform , addpost_form=addpost_form , updatephoto_form=updatephoto_form , profile_pic=profile_pic)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics' , picture_fn )
    output_size = (125 , 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_fn

@app.route('/home2', methods=['GET', 'POST'])
@login_required
def home2():
    return render_template('home2.html')


@app.route('/index2', methods=['GET', 'POST'])
@login_required
def index2():
    return render_template('index2.html')


def addpost( userid , title , content):
    new_post = Post(userid , title, content)
    db.session.add(new_post)
    db.session.commit()

'''