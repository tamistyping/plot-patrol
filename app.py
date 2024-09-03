from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///property_db.db'
app.config['SECRET_KEY'] = 'a_secret_key'  
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models.user import User
from models.property import Property
from routes.auth_routes import *
from routes.property_routes import *
from routes.user_routes import * 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all() 

if __name__ == "__main__":
    app.run(debug=True)