from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = ".database.db"


def create_app():
    app = Flask(__name__)
    #Generate a key with python
    #Import secrets
    #secrets.token_hex(16)
    app.config['SECRET_KEY'] = 'e13e220548305f2ee45b3537d1dcdf5c'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)
    
    #The login manager function contains the code that lets your application and Flask-Login work together, such as how to load a user from an ID,
    #where to send users when they need to log in, and the like.
    login_manager = LoginManager()    
    login_manager.login_view = 'auth.login'
    #We provide it with app it is the database where queries search for ID's and other stuff
    login_manager.init_app(app)
    
    #Here automatically it takes the id just we give it how it is defined "The name id or user_id" ect ...
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#Database creation
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
