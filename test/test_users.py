""" import unittest
from app import app

class TestUsers(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
        return super().setUp()
    

    def test_user_created_successfully(self):
        pass

    def test_role_is_correct(self):
        pass

    def test_user_deleted_successfully(self):
        pass

    def test_user_updated_successfully(self):
        pass

    def test_user_obtained_successfully(self):
        pass

 """