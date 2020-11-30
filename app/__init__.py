from flask_restplus import Api
from flask import Blueprint
from app.api.accounts.views import acc_api

v1_blueprint = Blueprint("api", __name__)
api_v1 = Api(v1_blueprint,
             title='MOVIE TICKET APP FLASK API',
             version='1.0',
             description='a backend api for the movie ticket app')
api_v1.add_namespace(acc_api, path="/auth")
