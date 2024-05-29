import unittest
from decimal import Decimal
from datetime import datetime
import json

from app import app
from services.bulletins.models.bulletin_model import BulletinModel
from services.bulletins.entities.bulletin import Bulletin

from database.db_connection import get_connection


class TestBulletins(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()


        # This user is created because
        login_data = {
            'email': 'test@gmail.com',
            'password': '12345678',
        }
        headers = {
            'Content-Type': 'application/json'
        }
            
        login_request = self.client.post('http://localhost:5000/auth/login', data=json.dumps(login_data), headers=headers)

        loggedin_user = json.loads(login_request.data)
        self.user_id = loggedin_user["id"]


    def tearDown(self):
        conn = get_connection()
        cursor = conn.cursor()
        """ 
        cursor.execute("DELETE FROM bulletins WHERE registration = '4567-ABG'")
        cursor.execute("DELETE FROM bulletins WHERE registration = '4567-SQW'")
        cursor.execute("DELETE FROM bulletins WHERE registration = '0000999'")
         """
        conn.commit()
        cursor.close()
        conn.close() 

        self.client.get('http://localhost:5000/auth/logout')
        
      
    def test_create_bulletin(self):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        bulletins_data = {
            'responsible_id': self.user_id,
            'zone_name': 'Plaza Castilla',
            'registration': '4567-ABG',
            'precept': "Se salta el tráfico",
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
        self.assertEqual(response_data["zone"], 'Plaza Castilla')
        self.assertEqual(response_data["registration"], "4567-ABG")
        self.assertEqual(response_data["paid"], False)
        self.assertEqual(response_data["brand"], None)
        self.assertEqual(response_data["model"], None)
        self.assertEqual(response_data["color"], None)
        self.assertEqual(response_data["created_at"], created_at)

        bulletin: Bulletin = BulletinModel.get_bulletin(id)

        self.assertIsNotNone(bulletin)
        self.assertEqual(bulletin.responsible.name, 'test')
        self.assertEqual(bulletin.zone.name, 'Plaza Castilla')
        self.assertEqual(bulletin.registration, "4567-ABG")
        self.assertEqual(bulletin.paid, False)
        self.assertEqual(bulletin.brand, None)
        self.assertEqual(bulletin.model, None)
        self.assertEqual(bulletin.color, None)
        self.assertEqual(bulletin.created_at.strftime("%Y-%m-%d %H:%M"), created_at)




    def test_create_incorrect_bulletin(self):
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


    def test_pay_bulletin(self):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        bulletins_data = {
            'responsible_id': self.user_id,
            'zone_name': 'Plaza Castilla',
            'registration': '4567-ABG',
            'precept': "Se salta el tráfico",
            'brand': 'Toyota',
            'model': 'C-3',
            'color': 'rojo',
            'created_at': created_at
        }
        headers = {
            'Content-Type': 'application/json'
        }
        
        
        response = self.client.post('http://localhost:5000/bulletins/create', data=json.dumps(bulletins_data), headers=headers, follow_redirects=True)
        

        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.data)
        id = response_data["id"]

        bulletin: Bulletin = BulletinModel.get_bulletin(id)

        self.assertIsNotNone(bulletin)
        self.assertEqual(bulletin.paid, False)

        # Construct form data for payment
        payment_data = {
            'payment_method': 'CASH',
            'price': '0.70',
            'duration': 'MEDIA HORA'
        }
    

        url = f'http://localhost:5000/bulletins/pay/{id}'
        
        response = self.client.post(url, data=payment_data, headers= {
                'Content-Type': 'multipart/form-data', 
            })
        self.assertEqual(response.status_code, 200)

        bulletin = BulletinModel.get_bulletin(id)

        self.assertIsNotNone(bulletin)
        self.assertEqual(bulletin.paid, True)


    def test_get_bulletins_by_registration(self):
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        bulletins_data = {
            'responsible_id': self.user_id,
            'zone_name': 'Plaza Castilla',
            'registration': '9999ABC',
            'precept': "Se salta el tráfico",
            'created_at': created_at
        }
        headers = {
            'Content-Type': 'application/json'
        }
        
        
        response = self.client.post('http://localhost:5000/bulletins/create', data=json.dumps(bulletins_data), headers=headers, follow_redirects=True)
        
        
        self.assertEqual(response.status_code, 200)
        registration = "9999ABC"
        url = f'http://localhost:5000/bulletins/get-bulletins-by-registration/{registration}'
        
        response = self.client.get(url)
        bulletins_found = response.json
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(bulletins_found) > 0)

