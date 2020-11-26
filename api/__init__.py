from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import configs


db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(configs[configuration])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    return app
