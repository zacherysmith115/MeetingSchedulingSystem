from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# app config and db initialization #
app = Flask(__name__)
app.config['SECRET_KEY'] = '653d72d9f6ed01acf0d4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'false'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'


from mss.Routes import AdminRoutes, ClientRoutes, LoginRoutes, UtilityRoutes