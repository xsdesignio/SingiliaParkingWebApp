from ..entities.schedule import ScheduleDay, ScheduleWeek
from psycopg2 import extras


from database.db_connection import get_connection

from database.base_model import BaseModel

WEEK_SCHEDULE_ID: int = 1

class ScheduleModel(BaseModel):

    @classmethod
    def update_element(cls, table, data, id):
        """
            Helper method for other functions
        """


        keys = data.keys()
        values = [data[key] for key in keys]
        set_clause = ", ".join([f"{key} = %s" for key in keys])
        query = f"UPDATE {table} SET {set_clause} WHERE id = %s"

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, values + [id])
            conn.commit()
            conn.close()
        except Exception as exception:
            print("update_element: ", exception)


    @classmethod
    def get_week_schedule(cls) -> ScheduleWeek:
        # Get week schedule
        result = cls.get_element('weekSchedule', id=WEEK_SCHEDULE_ID)
        days_keys = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        week_days = {}

        for day in days_keys:
            daily_schedule_id = result[day]
            daily_schedule = cls.get_element('dailySchedule', id=daily_schedule_id) if daily_schedule_id else None
            
            if daily_schedule:
                week_days[day] = ScheduleDay(id=daily_schedule["id"], openTime=daily_schedule['opentime'], closeTime=daily_schedule['closetime'])
            else:
                week_days[day] = None

        week_schedule = ScheduleWeek(**week_days)
        return week_schedule

    @classmethod
    def get_daily_schedule(cls, day_id: int) -> ScheduleDay:
        result = cls.get_element('dailySchedule', id=day_id)
        if result:
            return ScheduleDay(id = result["id"], openTime=result['openTime'], closeTime=result['closetime'])
        return None

    @classmethod
    def update_daily_schedule(cls, day_id: int, open_time: str, close_time: str) -> None:
        data = {
            'openTime': open_time,
            'closeTime': close_time
        }
        cls.update_element('dailySchedule', data, id=day_id)
        
    
    @classmethod
    def create_daily_schedule(cls, open_time: str, close_time: str) -> int:
        query = "INSERT INTO dailySchedule (opentime, closetime) VALUES (%s, %s) RETURNING id"
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (open_time, close_time))
            new_id = cursor.fetchone()['id']
            conn.commit()
            conn.close()
            return new_id
        except Exception as e:
            print(f"Error creating daily schedule: {e}")
            raise

    @classmethod
    def update_week_schedule(cls, day_key: str, daily_schedule_id: int) -> None:
        query = f"UPDATE weekSchedule SET {day_key} = %s WHERE id = %s"
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (daily_schedule_id, WEEK_SCHEDULE_ID))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error updating week schedule: {e}")
            raise