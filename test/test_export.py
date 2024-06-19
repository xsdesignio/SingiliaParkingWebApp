from app import app
import unittest
import json
import random
import unittest
import json
import os
from datetime import datetime, timedelta

from app import app
from services.tickets.models.ticket_model import TicketModel
from services.tickets.models.available_ticket_model import AvailableTicketModel
from services.bulletins.models.bulletin_model import BulletinModel
from services.bulletins.models.available_bulletin_model import AvailableBulletinModel
from database.db_connection import get_connection

class TestExport(unittest.TestCase):
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

        self.assertIsNotNone(self.user_id)

        self.generate_sample_data()

    def tearDown(self):
        # Delete any generated data left
        self.delete_sample_data()

    def generate_sample_data(self):
        periods = [
            ('2023-02-01', '2023-03-01'),
            ('2023-04-02', '2023-06-01'),
            ('2023-07-02', '2023-09-01'),
            ('2023-10-02', '2024-01-01')
        ]
        
        for start_date_str, end_date_str in periods:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            # Create tickets
            available_tickets = AvailableTicketModel.get_available_tickets()

            for available_ticket in available_tickets:
                ticket_data = {
                    'responsible_id': self.user_id,
                    'registration': '0000TES',
                    'duration': available_ticket["duration"],
                    'price': str(available_ticket["price"]),
                    'payment_method': 'CASH',
                    'zone': 'Plaza Castilla',
                    'created_at': start_date.strftime("%Y-%m-%d %H:%M")
                }
                response = self.client.post('http://localhost:5000/tickets/create', data=json.dumps(ticket_data), headers={'Content-Type': 'application/json'}, follow_redirects=True)
                self.assertEqual(response.status_code, 200)

            # Create bulletins
            available_bulletins = AvailableBulletinModel.get_available_bulletins()

            for bulletin_type in available_bulletins:
                bulletin_data = {
                    'responsible_id': self.user_id,
                    'zone_name': 'Plaza Castilla',
                    'registration': '0000TES',
                    'precept': 'Rebasar horario de permanencia',
                    'created_at': start_date.strftime("%Y-%m-%d %H:%M")
                }
                response = self.client.post('http://localhost:5000/bulletins/create', data=json.dumps(bulletin_data), headers={'Content-Type': 'application/json'}, follow_redirects=True)
                self.assertEqual(response.status_code, 200)



    def delete_sample_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tickets WHERE registration LIKE '0000TES'")
        cursor.execute("DELETE FROM bulletins WHERE registration LIKE '0000TES'")
        
        conn.commit()
        cursor.close()
        conn.close()

    def test_tickets_export_csv(self):
        # Restart tickets and bulletins data
        data = {
            'start_date': '2023-01-01',
            'end_date': '2024-03-01',
            'extension': 'csv'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Verify tickets have been deleted
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*) FROM tickets 
            WHERE registration LIKE '0000TES'
            AND created_at > '{data["start_date"]}'
            AND created_at < '{data["end_date"]}'
            """)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertNotEqual(count, 0)

        response = self.client.post('/export/export-database-tickets', data=data, headers=headers)
        
        file_name = response.headers['Content-Disposition'].split('filename=')[-1].strip('"')
        export_path = f'static/exports/{ file_name }'

        self.assertEqual(response.status_code, 200)
        self.assertTrue("text/csv" in response.headers['Content-Type'])
        self.assertTrue(".csv" in file_name)
        self.assertFalse(os.path.exists(export_path))

        # Verify tickets have been deleted
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT COUNT(*) FROM tickets 
            WHERE registration LIKE '0000TES'
            AND created_at > '{data["start_date"]}'
            AND created_at < '{data["end_date"]}'
            """)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertNotEqual(count, 0)
        

    def test_bulletins_export_csv(self):
        # Restart tickets and bulletins data
        
        data = {
            'start_date': '2023-03-02',
            'end_date': '2024-06-01',
            'extension': 'csv'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Verify tickets have been deleted
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*) FROM bulletins 
            WHERE registration LIKE '0000TES'
            AND created_at > '{data["start_date"]}'
            AND created_at < '{data["end_date"]}'
            """)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertNotEqual(count, 0)

        response = self.client.post('/export/export-database-bulletins', data=data, headers=headers)
        
        file_name = response.headers['Content-Disposition'].split('filename=')[-1].strip('"')
        export_path = f'static/exports/{ file_name }'

        self.assertEqual(response.status_code, 200)
        self.assertTrue("text/csv" in response.headers['Content-Type'])
        self.assertTrue(".csv" in file_name)
        self.assertFalse(os.path.exists(export_path))

        # Verify tickets have been deleted
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*) FROM bulletins 
            WHERE registration LIKE '0000TES'
            AND created_at > '{data["start_date"]}'
            AND created_at < '{data["end_date"]}'
            """)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertNotEqual(count, 0)
        


    def test_tickets_export_delete(self):
        # Restart tickets and bulletins data
        data = {
            'start_date': '2023-06-02',
            'end_date': '2024-09-01',
            'extension': 'csv',
            'delete': 'true'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = self.client.post('/export/export-database-tickets', data=data, headers=headers)
        
        file_name = response.headers['Content-Disposition'].split('filename=')[-1].strip('"')
        export_path = f'static/exports/{ file_name }'

        self.assertEqual(response.status_code, 200)
        self.assertTrue("text/csv" in response.headers['Content-Type'])
        self.assertTrue(".csv" in file_name)
        
        # Verify tickets have been deleted
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*) FROM tickets 
            WHERE registration LIKE '0000TES'
            AND created_at > '{data["start_date"]}'
            AND created_at < '{data["end_date"]}'
            """)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertEqual(count, 0)

    def test_bulletins_export_delete(self):

        # Restart tickets and bulletins data
        data = {
            'start_date': '2023-09-02',
            'end_date': '2024-01-01',
            'extension': 'csv',
            'delete': 'true'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.client.post('/export/export-database-bulletins', data=data, headers=headers)
        
        file_name = response.headers['Content-Disposition'].split('filename=')[-1].strip('"')
        export_path = f'static/exports/{ file_name }'

        self.assertEqual(response.status_code, 200)
        self.assertTrue("text/csv" in response.headers['Content-Type'])
        self.assertTrue(".csv" in file_name)
        
        # Verify bulletins have been deleted
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*) FROM bulletins 
            WHERE registration LIKE '0000TES'
            AND created_at > '{data["start_date"]}'
            AND created_at < '{data["end_date"]}'
            """)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        self.assertEqual(count, 0)
