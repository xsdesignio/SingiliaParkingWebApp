import unittest
from decimal import Decimal
from datetime import datetime
import json

from app import app
from services.tickets.models.ticket_model import TicketModel
from services.tickets.models.available_ticket_model import AvailableTicketModel
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

        conn = get_connection()
        cursor = conn.cursor()
        # Delete registrations used during the test
        cursor.execute("DELETE FROM tickets WHERE registration = '4567-ABG'")
        cursor.execute("DELETE FROM tickets WHERE registration = '4567-SQW'")
        conn.commit()
        cursor.close()
        conn.close() 


        self.client.get('http://localhost:5000/auth/logout')
        
        

    def test_create_all_available_tickets(self):

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        available_tickets = AvailableTicketModel.get_available_tickets()
        
        for available_ticket in available_tickets:
            ticket_data = {
                'registration': '4567-ABG',
                'duration': available_ticket["duration"],
                # Converting price to string because Decimal is not serializable
                'price': str(available_ticket["price"]), 
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
            self.assertEqual(ticket.duration, available_ticket["duration"])
            self.assertEqual(ticket.price, Decimal(available_ticket["price"]))
            self.assertEqual(ticket.payment_method, PaymentMethod.CASH)
            self.assertEqual(ticket.zone.name, "Plaza Castilla")
            self.assertEqual(ticket.created_at.strftime("%Y-%m-%d %H:%M"), created_at)

    def test_create_incorrect_ticket(self):
        ticket_data = {
            'registration': '4567-ABG',
            'duration': "MEDIA HORA",
            'price': 0.70,
            # 'payment_method': 'CASH',
            # 'zone': 'Plaza Castilla',
        } # payment_method and zone are required

        headers = {
            'Content-Type': 'application/json'
        }
            
        response = self.client.post('http://localhost:5000/tickets/create', data=json.dumps(ticket_data), headers=headers)
        self.assertEqual(response.status_code, 308)

