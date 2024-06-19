import unittest
import json
from app import app
from database.db_connection import get_connection
from psycopg2 import extras
from services.schedule.models.schedule_model import ScheduleModel
from services.schedule.entities.schedule import DailySchedule
from datetime import datetime

class TestSchedule(unittest.TestCase):
    
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

        # Login the user and store the user_id
        login_data = {
            'email': 'test@gmail.com',
            'password': '12345678',
        }
        headers = {
            'Content-Type': 'application/json'
        }
            
        login_request = self.client.post('/auth/login', data=json.dumps(login_data), headers=headers)

        self.assertEqual(login_request.status_code, 200, "Login request failed")

        loggedin_user = json.loads(login_request.data)
        self.user_id = loggedin_user.get("id")
        self.assertIsNotNone(self.user_id, "User ID not found in login response")

        # Ensure the database is in a known state
        self.reset_database()

    def tearDown(self):
        # Close the database connection
        self.reset_database()

    def reset_database(self):
        """Utility method to reset the database state before each test"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Clear the weekSchedule and dailySchedule tables
        cursor.execute("DELETE FROM weekSchedule")
        cursor.execute("DELETE FROM dailySchedule")
        
        # Re-insert a default week schedule
        cursor.execute("""
            INSERT INTO weekSchedule (id, monday, tuesday, wednesday, thursday, friday, saturday, sunday) 
            VALUES (1, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
        """)
        
        conn.commit()
        cursor.close()
        conn.close()

    def test_add_open_span_to_weekday(self):
        open_span_data = {
            "openTime": "09:00:00",
            "closeTime": "14:00:00"
        }
        open_span_data2 = {
            "openTime": "16:00:00",
            "closeTime": "21:00:00"
        }


        day_index = 0 # Monday

        # Adding to open spans to monday
        response = self.client.post(f'/schedule/add/{day_index}/', data=open_span_data)
        response = self.client.post(f'/schedule/add/{day_index}/', data=open_span_data2)

        # Adding another open spans to tuesday
        response = self.client.post(f'/schedule/add/{day_index+1}/', data=open_span_data)
        self.assertEqual(response.status_code, 301)

        # Verify the open span was added

        # Obtains dailySchedule id
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute("SELECT monday FROM weekSchedule WHERE id = 1")
        monday_schedule_id = cursor.fetchone()["monday"]

        cursor.execute("SELECT tuesday FROM weekSchedule WHERE id = 1")
        tuesday_schedule_id = cursor.fetchone()["tuesday"]
        
        cursor.close()
        conn.close()

        # Obtains daily_schedule object
        monday_schedule: DailySchedule = ScheduleModel.get_daily_schedule(monday_schedule_id)
        self.assertIsNotNone(monday_schedule)


        open_spans = monday_schedule.openSpans
        self.assertIsNotNone(open_spans)
        self.assertEqual(len(open_spans), 2)
        self.assertEqual(open_spans[1].openTime, datetime.strptime('16:00:00', '%H:%M:%S').time())
        self.assertEqual(open_spans[1].closeTime, datetime.strptime('21:00:00', '%H:%M:%S').time())

        # Obtains daily_schedule object
        tuesday_schedule: DailySchedule = ScheduleModel.get_daily_schedule(tuesday_schedule_id)
        self.assertIsNotNone(monday_schedule)

        open_spans = tuesday_schedule.openSpans
        self.assertIsNotNone(open_spans)
        self.assertEqual(len(open_spans), 1)
        self.assertEqual(open_spans[0].openTime, datetime.strptime('09:00:00', '%H:%M:%S').time())
        self.assertEqual(open_spans[0].closeTime, datetime.strptime('14:00:00', '%H:%M:%S').time())

        cursor.close()
        conn.close()

        self.reset_database()

    def test_remove_open_span_to_week_day(self):

        open_span_data = {
            "openTime": "09:00:00",
            "closeTime": "14:00:00"
        }
        open_span_data2 = {
            "openTime": "16:00:00",
            "closeTime": "21:00:00"
        }

        day_index = 0 # Monday

        # Adding to open spans to monday
        response = self.client.post(f'/schedule/add/{day_index}/', data=open_span_data)
        response = self.client.post(f'/schedule/add/{day_index}/', data=open_span_data2)

        day_index = 0 # Monday
        daily_schedule_id_query = "SELECT monday FROM weekSchedule WHERE id = 1"
        
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute(daily_schedule_id_query)
        daily_schedule_id = cursor.fetchone()['monday']

        cursor.close()
        conn.close()
        
        # Obtains daily_schedule object
        daily_schedule: DailySchedule = ScheduleModel.get_daily_schedule(daily_schedule_id)
        self.assertIsNotNone(daily_schedule)

        open_spans = daily_schedule.openSpans
        self.assertIsNotNone(open_spans)
        self.assertEqual(len(open_spans), 2)
        self.assertEqual(open_spans[0].openTime, datetime.strptime('09:00:00', '%H:%M:%S').time())
        self.assertEqual(open_spans[0].closeTime, datetime.strptime('14:00:00', '%H:%M:%S').time())
        self.assertEqual(open_spans[1].openTime, datetime.strptime('16:00:00', '%H:%M:%S').time())
        self.assertEqual(open_spans[1].closeTime, datetime.strptime('21:00:00', '%H:%M:%S').time())


        response = self.client.post(f'/schedule/remove/{day_index}/')
        self.assertEqual(response.status_code, 301)

        # Verify the open span was removed
        daily_schedule: DailySchedule = ScheduleModel.get_daily_schedule(daily_schedule_id)
        
        open_spans = daily_schedule.openSpans
        self.assertIsNotNone(open_spans)
        self.assertEqual(len(open_spans), 1)
        self.assertEqual(open_spans[0].openTime, datetime.strptime('09:00:00', '%H:%M:%S').time())
        self.assertEqual(open_spans[0].closeTime, datetime.strptime('14:00:00', '%H:%M:%S').time())


        self.reset_database()


    def test_get_empty_week_schedule(self):

        # Checking week_schedule obtains the data
        response = self.client.get('/schedule/obtain/')
        self.assertEqual(response.status_code, 200)

        week_schedule = json.loads(response.data)
        self.assertIn('monday', week_schedule)
        self.assertIn('tuesday', week_schedule)
        self.assertIn('wednesday', week_schedule)
        self.assertIn('thursday', week_schedule)
        self.assertIn('friday', week_schedule)
        self.assertIn('saturday', week_schedule)
        self.assertIn('sunday', week_schedule)


    def test_get_week_schedule(self):

        # Adding some data to the week_schedule
        open_span_data = {
            "openTime": "09:00:00",
            "closeTime": "18:00:00"
        }

        day_index = 0 # Monday
        for day_index in range(0, 7):
            response = self.client.post(f'/schedule/add/{day_index}/', data=open_span_data)


        # Checking week_schedule obtains the data
        response = self.client.get('/schedule/obtain/')
        self.assertEqual(response.status_code, 200)

        week_schedule = json.loads(response.data)
        self.assertIn('monday', week_schedule)
        self.assertIn('tuesday', week_schedule)
        self.assertIn('wednesday', week_schedule)
        self.assertIn('thursday', week_schedule)
        self.assertIn('friday', week_schedule)
        self.assertIn('saturday', week_schedule)
        self.assertIn('sunday', week_schedule)

        self.reset_database()


if __name__ == '__main__':
    unittest.main()
