from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///property_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
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

@app.route('/')
@login_required
def index():
    properties = Property.query.filter_by(owner_id=current_user.id).all()
    total_property_value = sum(property.value for property in properties)
    return render_template('index.html', properties=properties, total_property_value=total_property_value)

if __name__ == "__main__":
    app.run(debug=True)
