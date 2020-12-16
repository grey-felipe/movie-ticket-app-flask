from flask_restplus import Namespace, fields


class AccountsDto:
    acc_namespace = Namespace(
        "account", description="Accounts data access object")
    account = acc_namespace.model("account", {
        "username": fields.String(required=True, description="User username"),
        "email": fields.String(required=True, description="User email"),
        "is_admin": fields.Boolean(required=True, description="User permission for admin rights"),
        "password": fields.String(required=True, description="User password"),
        "avatar": fields.String(required=False, description="User image"),
        "bio": fields.String(required=False, description="User bio"),
        "created_at": fields.DateTime(required=False, description="The time the user was created"),
        "updated_at": fields.DateTime(required=False, description="The time the user was updated"),
    })
