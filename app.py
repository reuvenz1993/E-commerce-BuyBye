from ecommerce import app,db
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from ecommerce.models import *
from werkzeug.security import generate_password_hash, check_password_hash
import ecommerce.views
import ecommerce.api

web: gunicorn app:app
if __name__ == '__main__':
    app.run(debug=True)