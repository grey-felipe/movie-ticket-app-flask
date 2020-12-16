from flask_testing import TestCase
from app.api import db
from manage import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object("config.TESTING_CONFIG")
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
