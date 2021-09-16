from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'rpykgmslsrlrtpogh'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # Whatever the prefix is will be required to route to that view from the URL ie. /auth/login

    from .models import User, Note
    # dot source basically then * for all

    #.model is a relative import AKA relative to this files position
    # the purpose of importing is to execute the classes inside

    create_database(app)


    login_manager = LoginManager()
    # instantiates login manager object
    login_manager.login_view = 'auth.login'
    # where should flask redirect if not logged in
    login_manager.init_app(app)
    # tell it what app we're using

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    # get() will look for primary key and check if equal to whatever is passed
    #

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

