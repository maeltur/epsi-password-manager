from flask import Flask
from flask_mysqldb import MySQL
from passwordmanager import credentialsmsql


def create_app():
    app = Flask(__name__)
    app.config = {'MYSQL_HOST': '192.168.1.30',
                  'MYSQL_USER': credentialsmsql.user,
                  'MYSQL_PASSWORD': credentialsmsql.password,
                  'MYSQL_DB': 'passmanager',
                  'SECRET_KEY': '_5#y2L"F4Q8zec]'}
    #mysql = MySQL(app)
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # BLueprint for passwordmanager part
    from .passmanager import passmanager as passmanager_blueprint
    app.register_blueprint(passmanager_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.run()
