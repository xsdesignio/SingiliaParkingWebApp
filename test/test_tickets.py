import unittest
from decimal import Decimal
from datetime import datetime
import json

from app import app
from services.tickets.models.ticket_model import TicketModel
from services.tickets.entities.ticket import Ticket


from database.db_connection import get_connection
from services.utils.payment_methods import PaymentMethod

class TestTickets(unittest.TestCase):
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

        """ 
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE name = 'test'")
        cursor.execute("DELETE FROM tickets WHERE registration = '4567-ABG'")
        cursor.execute("DELETE FROM tickets WHERE registration = '4567-SQW'")
        cursor.execute("DELETE FROM users WHERE name = 'test'")

        conn.commit()
        cursor.close()
        conn.close() 

        """

        self.client.get('http://localhost:5000/auth/logout')
        
        

    def test_create_ticket(self):

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        ticket_data = {
            'registration': '4567-ABG',
            'duration': "MEDIA HORA",
            'price': 0.70,
            'payment_method': 'CASH',
            'zone': 'Plaza Castilla',
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
        self.assertEqual(ticket.duration, "MEDIA HORA")
        self.assertEqual(ticket.price, Decimal('0.70'))
        self.assertEqual(ticket.payment_method, PaymentMethod.CASH)
        self.assertEqual(ticket.zone.name, "Plaza Castilla")
        self.assertEqual(ticket.created_at.strftime("%Y-%m-%d %H:%M"), created_at)

        # Creating the ticket giving the responsible_id and created_at

        ticket_data_2 = {
            'responsible_id': self.user_id,
            'registration': '4567-SQW',
            'duration': "MEDIA HORA",
            'price': 0.70,
            'payment_method': 'CARD',
            'zone': 'Plaza Castilla',
            'created_at': created_at
        }

        response_2 = self.client.post('http://localhost:5000/tickets/create', data=json.dumps(ticket_data_2), headers=headers, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response_2.data)
        id = response_data["id"]

        ticket: Ticket = TicketModel.get_ticket(id)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.registration, "4567-SQW")
        self.assertEqual(ticket.duration, "MEDIA HORA")
        self.assertEqual(ticket.price, Decimal('0.70'))
        self.assertEqual(ticket.payment_method, PaymentMethod.CARD)
        self.assertEqual(ticket.zone.name, "Plaza Castilla")
        self.assertEqual(ticket.created_at.strftime("%Y-%m-%d %H:%M"), created_at)

    def test_create_incorrect_ticket(self):
        ticket_data = {
            'registration': '4567-ABG',
            'duration': "MEDIA HORA",
            'price': 0.70,
        }
        headers = {
            'Content-Type': 'application/json'
        }
            
        response = self.client.post('http://localhost:5000/tickets/create', data=json.dumps(ticket_data), headers=headers)
        self.assertEqual(response.status_code, 308)

