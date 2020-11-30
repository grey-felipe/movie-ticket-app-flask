from app.api.accounts.service import save_token
import unittest
import json
import datetime

from app.api import db
from app.api.accounts.models import User
from tests.base import BaseTestCase


class TestAccountsTestCase(BaseTestCase):

    test_token = """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
    .eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ
    .SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"""

    @staticmethod
    def register_valid_user(self):
        return self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(dict(
                username="tester",
                email="test@gmail.com",
                is_admin=False,
                password="password",
                avatar="http://test-image.com",
                bio="This is a test bio"
            )),
            content_type="application/json")

    @staticmethod
    def register_invalid_user(self):
        return self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(dict(
                username="",
                email="",
                is_admin=False,
                password="password",
                avatar="http://test-image.com",
                bio="This is a test bio"
            )),
            content_type="application/json")

    def test_encode_auth_token(self):
        user = User(username="tester",
                    email="test@gmail.com",
                    is_admin=False,
                    password="password",
                    avatar="http://test-image.com",
                    bio="This is a test bio",
                    created_at=datetime.datetime.now())
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id, user.is_admin)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(username="tester",
                    email="test@email.com",
                    is_admin=False,
                    password="password",
                    avatar="http://test-image.com",
                    bio="This is a test bio",
                    created_at=datetime.datetime.now())
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id, user.is_admin)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(len(user.decode_auth_token(auth_token)) == 2)

    def test_user_sign_up(self):
        with self.client:
            response = self.register_valid_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(isinstance(data["token"], str))
            self.assertEqual(response.status_code, 201)

    def test_user_already_exists(self):
        with self.client:
            self.register_valid_user(self)
            response = self.register_valid_user(self)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["message"],
                             "A user with this email already exists")

    def test_registration_empty_string(self):
        response = self.register_invalid_user(self)
        self.assertEqual(response.status_code, 400)

    def test_save_token(self):
        result = save_token(self.test_token)
        self.assertEqual(result[1], 201)

    def test_save_token_exception(self):
        save_token(self.test_token)
        result = save_token(self.test_token)
        self.assertEqual(result[1], 400)


if __name__ == '__main__':
    unittest.main()
