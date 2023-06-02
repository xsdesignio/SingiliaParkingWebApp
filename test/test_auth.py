from psycopg2 import connect
import unittest
import json
from app import app
from models.user_model import UserModel

dbname = 'parkingcontroldb'
dbuser = 'pablo'
password = 'jd3_Ljks2h'

class TestAuth(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        conn = connect(dbname = dbname, user = dbuser, password =password)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE name = 'test'")

        conn.commit()
        cursor.close()
        conn.close()
        
    
    def test_signup(self):
        data = {
            'role': 'ADMIN',
            'name': 'test',
            'email': 'example@gmail.com',
            'password': 'password',
            'secret_code': 4578
        }
        headers = {
            'Content-Type': 'application/json'
        }
            
        response = self.client.post('http://localhost:5000/auth/signup', data=json.dumps(data), headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        
        user = UserModel.get_validated_user('example@gmail.com', 'password')
        self.assertIsNotNone(user)

        with self.client.session_transaction() as session:

            self.assertTrue('role' in session)
            self.assertEqual(session['role'], 'ADMIN')

            self.assertTrue('name' in session)
            self.assertEqual(session['name'], 'test')

            self.assertTrue('email' in session)
            self.assertEqual(session['email'], 'example@gmail.com')
        

    def test_login_logout(self):
        data = {
            'role': 'ADMIN',
            'name': 'test',
            'email': 'example2@gmail.com',
            'password': 'password',
            'secret_code': 4578
        }
        headers = {
            'Content-Type': 'application/json'
        }
            
        self.client.post('http://localhost:5000/auth/signup', data=json.dumps(data), headers=headers, follow_redirects=True)
        
        with self.client.session_transaction() as session:

            self.assertTrue('role' in session)
            self.assertEqual(session['role'], 'ADMIN')

            self.assertTrue('name' in session)
            self.assertEqual(session['name'], 'test')

            self.assertTrue('email' in session)
            self.assertEqual(session['email'], 'example2@gmail.com')

        
        self.client.get('http://localhost:5000/auth/logout')

        with self.client.session_transaction() as session:

            self.assertFalse('role' in session)

            self.assertFalse('name' in session)

            self.assertFalse('email' in session)

        
        # create user
        data = {
            'email': 'example2@gmail.com',
            'password': 'password'
        }
        headers = {
            'Content-Type': 'application/json'
        }

        # login with correct credentials
        response = self.client.post('http://localhost:5000/auth/login', data=json.dumps(data), headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Checking user added to session after login
        with self.client.session_transaction() as session:

            self.assertTrue('role' in session)
            self.assertEqual(session['role'], 'ADMIN')

            self.assertTrue('name' in session)
            self.assertEqual(session['name'], 'test')

            self.assertTrue('email' in session)
            self.assertEqual(session['email'], 'example2@gmail.com')

        # logout
        response = self.client.get('http://localhost:5000/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Checking user have been removed from session
        with self.client.session_transaction() as session:
            self.assertFalse('role' in session)
            self.assertFalse('name' in session)
            self.assertFalse('email' in session)



    def test_login_incorrect_password(self):
        # login with incorrect password
        data = {
            'email': 'example@gmail.com',
            'password': 'incorrect'
        }
        headers = {
            'Content-Type': 'application/json'
        }

        # login with correct credentials
        response = self.client.post('http://localhost:5000/auth/login', data=json.dumps(data), headers=headers, follow_redirects=True)
        

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertTrue("message" in data)

        with self.client.session_transaction() as session:
            self.assertFalse('role' in session)
            self.assertFalse('name' in session)
            self.assertFalse('email' in session)

    def test_login_nonexistent_user(self):
        # login with nonexistent user
        data = {
            'email': 'nonexistent',
            'password': 'password'
        }
        headers = {
            'Content-Type': 'application/json'
        }

        # login with correct credentials
        response = self.client.post('http://localhost:5000/auth/login', data=json.dumps(data), headers=headers, follow_redirects=True)
        
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertTrue("message" in data)

        with self.client.session_transaction() as session:
            self.assertFalse('role' in session)
            self.assertFalse('name' in session)
            self.assertFalse('email' in session)

