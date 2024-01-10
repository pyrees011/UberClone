from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.secret_key = 'dev'
    app.config['SECRET_KEY'] = 'dev'
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite3'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.config['DRIVER_PROFILE'] = "freeRide/static/images/driver_profile"
    db.init_app(app)


    from .auth import auth
    from .views_user import views_user
    from .views_driver import views_driver
    from .mongo_user import mongo_user
    from .mongo_driver import mongo_driver
    from .mongo import mongo

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views_user, url_prefix='/')
    app.register_blueprint(views_driver, url_prefix='/')
    app.register_blueprint(mongo_user, url_prefix='/')
    app.register_blueprint(mongo_driver, url_prefix='/')
    app.register_blueprint(mongo, url_prefix='/')

    with app.app_context():

        from .models import User, Driver, googleUser
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):

        from .models import User, Driver

        user = User.query.get(int(user_id))
        driver = Driver.query.get(int(user_id))

        if user:
            return user
        elif driver:
            return driver
        else:
            return None

    return app