import datetime

from app.api import db
from .models import User, TokenBlacklist

from utils.helpers import catch_empty_string


def add_account(data):
    user = User.query.filter_by(email=data["email"]).first()
    if user:
        response = {
            "status": "failed",
            "message": "A user with this email already exists"
        }
        return response, 400
    else:
        for k, v in data.items():
            if isinstance(data[k], str):
                if catch_empty_string(data[k]):
                    response = {
                        "status": "failed",
                        "message": "Please provide a valid '{}'".format(k)
                    }
                    return response, 400

        new_user = User(username=data["username"],
                        email=data["email"],
                        is_admin=data["is_admin"],
                        password=data["password"],
                        avatar=data["avatar"],
                        bio=data["bio"],
                        created_at=datetime.datetime.now())
        save_changes(new_user)
        token = generate_token(new_user.id, new_user.is_admin)
        response = {
            "status": "success",
            "message": "User created successfully",
            "token": token.decode(),
        }
        return response, 201


def generate_token(id, is_admin):
    try:
        auth_token = User.encode_auth_token(id, is_admin)
        return auth_token
    except Exception as e:
        return e


def save_token(token):
    blacklist_token = TokenBlacklist(token=token)
    try:
        save_changes(blacklist_token)
        response = {
            "status": "success",
            "message": "Token blacklisted"
        }
        return response, 201
    except Exception as e:
        response = {
            "status": "failed",
            "message": e
        }
        return response, 400


def save_changes(data):
    db.session.add(data)
    db.session.commit()
