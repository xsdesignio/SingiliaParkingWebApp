import unittest
from decimal import Decimal
from datetime import datetime
import json

from psycopg2 import connect

from app import app
from services.tickets.models.ticket_model import TicketModel
from services.tickets.entities.ticket import Ticket


from database.db_connection import get_connection

class TestTickets(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tickets WHERE registration = '4567-ABG'")
        cursor.execute("DELETE FROM tickets WHERE registration = '4567-SQW'")
        cursor.execute("DELETE FROM users WHERE name = 'test'")

        conn.commit()
        cursor.close()
        conn.close()

        self.client.get('http://localhost:5000/auth/logout')
        

    def test_create_ticket(self):

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

        ticket_data = {
            'registration': '4567-ABG',
            'duration': 30,
            'price': 0.90,
            'paid': True,
            'location': 'La Moraleda',
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        

        # Creating the ticket without the responsible_id and created_at
        response = self.client.post('http://localhost:5000/tickets/create', data=json.dumps(ticket_data), headers=headers, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.data)
        id = response_data["id"]

        ticket: Ticket = TicketModel.get_ticket(id)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.registration, "4567-ABG")
        self.assertEqual(ticket.duration, 30)
        self.assertEqual(ticket.price, Decimal('0.90'))
        self.assertEqual(ticket.paid, True)
        self.assertEqual(ticket.location, "La Moraleda")
        self.assertEqual(ticket.created_at.strftime("%Y-%m-%d %H:%M"), created_at)

        self.client.get('http://localhost:5000/auth/logout/', headers=headers, follow_redirects=True)


        # Creating the ticket giving the responsible_id and created_at

        ticket_data_2 = {
            'responsible_id': signedup_user["id"],
            'registration': '4567-SQW',
            'duration': 60,
            'price': 1.20,
            'paid': False,
            'location': 'La Moraleda',
            'created_at': created_at
        }

        response_2 = self.client.post('http://localhost:5000/tickets/create', data=json.dumps(ticket_data_2), headers=headers, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response_2.data)
        id = response_data["id"]

        ticket: Ticket = TicketModel.get_ticket(id)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.registration, "4567-SQW")
        self.assertEqual(ticket.duration, 60)
        self.assertEqual(ticket.price, Decimal('1.20'))
        self.assertEqual(ticket.paid, False)
        self.assertEqual(ticket.location, "La Moraleda")
        self.assertEqual(ticket.created_at.strftime("%Y-%m-%d %H:%M"), created_at)

        self.client.get('http://localhost:5000/auth/logout/', headers=headers, follow_redirects=True)


        


    def test_create_incorrect_ticket(self):
        
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

        ticket_data = {
            'registration': '4567-ABG',
            'duration': 30,
            'price': 0.90,
        }
        headers = {
            'Content-Type': 'application/json'
        }
            
        response = self.client.post('http://localhost:5000/tickets/create', data=json.dumps(ticket_data), headers=headers, follow_redirects=True)
        self.assertEqual(response.status_code, 400)


        self.client.get('http://localhost:5000/auth/logout/', headers=headers, follow_redirects=True)




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

        response = self.client.get('http://localhost:5000/auth/logout')
        
        ticket_data = {
            'responsible_id': signedup_user["id"],
            'registration': '4567-ABG',
            'duration': 30,
            'price': 0.90,
            'paid': True,
            'location': 'La Moraleda',
            'created_at': created_at
        }
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = self.client.post('http://localhost:5000/tickets/create', data=json.dumps(ticket_data), headers=headers, follow_redirects=True)
        self.assertEqual(response.history[0].status_code, 308)


    def test_pay_ticket(self):
        
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

        ticket_data = {
            'responsible_id': signedup_user["id"],
            'registration': '4567-ABG',
            'duration': 30,
            'price': 0.90,
            'paid': False,
            'location': 'La Moraleda',
            'created_at': created_at
        }
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = self.client.post('http://localhost:5000/tickets/create', data=json.dumps(ticket_data), headers=headers, follow_redirects=True)
        
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.data)
        id = response_data["id"]

        ticket: Ticket = TicketModel.get_ticket(id)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.paid, False)

        url = f'http://localhost:5000/tickets/pay/{id}'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)


        ticket = TicketModel.get_ticket(id)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.paid, True)


        self.client.get('http://localhost:5000/auth/logout/', follow_redirects=True)



    def test_error_on_pay_ticket_twice(self):
        
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

        ticket_data = {
            'responsible_id': signedup_user["id"],
            'registration': '4567-ABG',
            'duration': 30,
            'price': 0.90,
            'paid': True,
            'location': 'La Moraleda',
            'created_at': created_at
        }
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = self.client.post('http://localhost:5000/tickets/create', data=json.dumps(ticket_data), headers=headers, follow_redirects=True)
        
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.data)
        id = response_data["id"]

        ticket: Ticket = TicketModel.get_ticket(id)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.paid, True)


        url = f'http://localhost:5000/tickets/pay/{id}'
        response = self.client.post(url)
        
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(data["message"], "El ticket introducido ya ha sido pagado")


        ticket = TicketModel.get_ticket(id)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.paid, True)


        self.client.get('http://localhost:5000/auth/logout/', headers=headers, follow_redirects=True)

