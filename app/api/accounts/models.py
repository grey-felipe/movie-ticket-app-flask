import datetime
from datetime import timedelta
import jwt

from config import key
from app.api import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    @property
    def password(self):
        raise AttributeError("password:write only field")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password, 10).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(id, is_admin):
        try:
            payload = {
                "exp": datetime.datetime.now()+datetime.timedelta(days=5),
                "iat": datetime.datetime.now(),
                "user_id": id,
                "is_admin": is_admin
            }
            return jwt.encode(payload, key, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, key)
            blacklisted_token = TokenBlacklist.check_blacklist(payload)
            if blacklisted_token:
                return "This token has been blacklisted, please login again"
            else:
                return {
                    "user_id": payload["user_id"],
                    "is_admin": payload["is_admin"]
                }
        except jwt.ExpiredSignatureError:
            return "This token is expired, please login"
        except jwt.InvalidTokenError:
            return "This token is invalid."

    def __repr__(self) -> str:
        return "<User '{}'>".format(self.username)


class TokenBlacklist(db.Model):
    __tablename__ = "token_blacklist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return "<id: token: {}".format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        exists = TokenBlacklist.query.filter_by(token=str(auth_token)).first()
        if exists:
            return True
        else:
            return False
