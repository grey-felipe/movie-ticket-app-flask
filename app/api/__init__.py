from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import configs


db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(configs[configuration])
    db.init_app(app)
    bcrypt.init_app(app)
    return app
