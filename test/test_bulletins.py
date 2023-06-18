import unittest
from decimal import Decimal
from datetime import datetime
import json

from app import app
from bulletins.models.bulletin_model import BulletinModel
from bulletins.entities.bulletin import Bulletin

from database.db_connection import get_connection

class TestBulletins(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM bulletins WHERE registration = '4567-ABG'")
        cursor.execute("DELETE FROM users WHERE name = 'test'")

        conn.commit()
        cursor.close()
        conn.close()

        self.client.get('http://localhost:5000/auth/logout')
        

    def test_create_bulletin(self):

        # This user is created because
        signup_data = {
            'role': 'ADMIN',
            'name': 'test',
            'email': 'example@gmail.com',
            'password': 'password',
            'secret_code': 4578
        }
        headers = {
            'Content-Type': 'application/json'
        }
            
        signup_request = self.client.post('http://localhost:5000/auth/signup', data=json.dumps(signup_data), headers=headers)

        signedup_user = json.loads(signup_request.data)

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        bulletins_data = {
            'responsible_id': signedup_user["id"],
            'location': 'Plaza de Toros',
            'registration': '4567-ABG',
            'duration': 30,
            'price': 0.90,
            'paid': True,
            'brand': 'Toyota',
            'model': 'C-3',
            'signature': 'Pablo Cortés Rodríguez',
            'created_at': created_at
        }
        headers = {
            'Content-Type': 'application/json'
        }
        
        
        response = self.client.post('http://localhost:5000/bulletins/create', data=json.dumps(bulletins_data), headers=headers, follow_redirects=True)
        
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.data)
        id = response_data["id"]

        self.assertEqual(response_data["responsible"], 'test')
        self.assertEqual(response_data["location"], 'Plaza de Toros')
        self.assertEqual(response_data["registration"], "4567-ABG")
        self.assertEqual(response_data["duration"], 30)
        self.assertEqual(response_data["price"], "0.9")
        self.assertEqual(response_data["paid"], True)
        self.assertEqual(response_data["brand"], "Toyota")
        self.assertEqual(response_data["model"], "C-3")
        self.assertEqual(response_data["created_at"], created_at)

        bulletin: Bulletin = BulletinModel.get_bulletin(id)

        self.assertIsNotNone(bulletin)
        self.assertEqual(bulletin.responsible.name, 'test')
        self.assertEqual(bulletin.location, 'Plaza de Toros')
        self.assertEqual(bulletin.registration, "4567-ABG")
        self.assertEqual(bulletin.duration, 30)
        self.assertEqual(bulletin.price, Decimal('0.90'))
        self.assertEqual(bulletin.paid, True)
        self.assertEqual(bulletin.brand, "Toyota")
        self.assertEqual(bulletin.model, "C-3")
        self.assertEqual(bulletin.created_at.strftime("%Y-%m-%d %H:%M"), created_at)

        self.client.get('http://localhost:5000/auth/logout')



    def test_create_incorrect_bulletin(self):

        # This user is created because
        signup_data = {
            'role': 'ADMIN',
            'name': 'test',
            'email': 'example@gmail.com',
            'password': 'password',
            'secret_code': 4578
        }
        headers = {
            'Content-Type': 'application/json'
        }
            
        self.client.post('http://localhost:5000/auth/signup', data=json.dumps(signup_data), headers=headers)


        bulletin_data = {
            'registration': '4567-ABG',
            'duration': 30,
            'price': 0.90,
        }
        headers = {
            'Content-Type': 'application/json'
        }
            
        response = self.client.post('http://localhost:5000/bulletins/create', data=json.dumps(bulletin_data), headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 400)


        self.client.get('http://localhost:5000/auth/logout')
        


    def test_error_on_create_without_authentication(self):

        
        # This user is created because
        signup_data = {
            'role': 'ADMIN',
            'name': 'test',
            'email': 'example@gmail.com',
            'password': 'password',
            'secret_code': 4578
        }
        headers = {
            'Content-Type': 'application/json'
        }
            
        signup_request = self.client.post('http://localhost:5000/auth/signup', data=json.dumps(signup_data), headers=headers)

        signedup_user = json.loads(signup_request.data)

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        self.client.get('http://localhost:5000/auth/logout')
        bulletins_data = {
            'responsible_id': signedup_user["id"],
            'location': 'Plaza de Toros',
            'registration': '4567-ABG',
            'duration': 30,
            'price': 0.90,
            'paid': True,
            'brand': 'Toyota',
            'model': 'C-3',
            'signature': 'Pablo Cortés Rodríguez',
            'created_at': created_at
        }
        headers = {
            'Content-Type': 'application/json'
        }
        
        
        response = self.client.post('http://localhost:5000/bulletins/create', data=json.dumps(bulletins_data), headers=headers, follow_redirects=True)
        
        self.assertEqual(response.status_code, 401)


        
        
    def test_pay_bulletin(self):
        pass

    def test_error_on_pay_bulletin_twice(self):
        pass