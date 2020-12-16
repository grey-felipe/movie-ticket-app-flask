
from flask import request
from flask_restplus import Resource
from werkzeug.utils import validate_arguments
from .dto import AccountsDto
from .service import *


acc_api = AccountsDto.acc_namespace
ACCOUNT = AccountsDto.account


@acc_api.route("/register")
class RegisterUser(Resource):
    @acc_api.response(201, 'User successfully created.')
    @acc_api.doc("Creates new user")
    @acc_api.expect(ACCOUNT, validate=True)
    def post(self):
        data = request.get_json()
        return add_account(data)
