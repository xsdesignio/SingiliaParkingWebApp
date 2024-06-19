from psycopg2 import connect
import unittest
import json
from app import app
from services.users.models.user_model import UserModel

dbname = 'singiliaparking'
dbuser = 'pablo'
password = 'jd3_Ljks2h'



class TestAuth(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()


    def tearDown(self):
        con = connect(dbname=dbname, user=dbuser, password=password)
        cursor = con.cursor()
         
        cursor.execute("DELETE FROM users WHERE email = 'test@test.com'")
        
        con.commit()
        cursor.close()
        con.close()


    def test_signup(self):
        # Define test data
        test_data = {
            "role": "EMPLOYEE",
            "name": "test",
            "email": "test@test.com",
            "password": "test_password",
            "security_code": 4578
        }

        # Send a POST request to signup endpoint
        response = self.client.post('/auth/signup', json=test_data)
        data = json.loads(response.data.decode('utf-8'))

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "test")
        self.assertEqual(data["email"], "test@test.com")


    def test_login_logout(self):
        # Define test user
        test_user = UserModel.create_user(role="EMPLOYEE", name="test", email="test@test.com", password="test_password")

        # Define login data
        login_data = {
            "email": "test@test.com",
            "password": "test_password"
        }

        # Send a POST request to login endpoint
        response = self.client.post('/auth/login', json=login_data)
        data = json.loads(response.data.decode('utf-8'))

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "test")
        self.assertEqual(data["email"], "test@test.com")

        # Logout
        response = self.client.get('/auth/logout')
        self.assertEqual(response.status_code, 302)  # Check for redirection


    def test_create_login_incorrect_password(self):
        # Define test user
        test_user = UserModel.create_user(role="EMPLOYEE", name="test", email="test@example.com", password="test_password")

        # Define incorrect login data
        login_data = {
            "email": "test@test.com",
            "password": "incorrect_password"
        }

        # Send a POST request to login endpoint
        response = self.client.post('/auth/login', json=login_data)

        # Assertions
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
