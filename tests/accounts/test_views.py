import json
import unittest
from tests.base import BaseTestCase


class TestViewsTestCase(BaseTestCase):

    @staticmethod
    def valid_user():
        return {"username": "tester",
                "email": "test@gmail.com",
                "is_admin": False,
                "password": "password",
                "avatar": "http://test-image.com",
                "bio": "This is a test bio"}

    def test_registration_view(self):
        response = self.client.post("api/v1/auth/register",
                                    data=json.dumps(self.valid_user()),
                                    content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertTrue(isinstance(data["token"], str))
        self.assertEqual(response.status_code, 201)
