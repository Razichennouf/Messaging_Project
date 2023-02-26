from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'AZ55DAFRE5EF56AZ6E6AZ6E88AZEA7C7CAC7DA'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Message

    #create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    with app.app_context():
        db.create_all()
    return app

# This is an deprecated approach to create SQL ALchemy 
#Flask-SQLAlchemy 3 no longer accepts an app argument to methods like create_all. Instead, it always requires an active Flask application context.
#def create_database(app):
#    if not path.exists('./' + DB_NAME):
#        db.create_all(app=app)
#        print('Created Database!')
