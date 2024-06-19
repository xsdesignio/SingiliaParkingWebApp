from ..entities.schedule import OpenSpan, DailySchedule, ScheduleWeek
from psycopg2 import extras
from datetime import datetime
from time import time
import json
from database.db_connection import get_connection

import re
from database.base_model import BaseModel

WEEK_SCHEDULE_ID: int = 1

class ScheduleModel(BaseModel):

    days_keys = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    @classmethod
    def get_week_schedule(cls) -> ScheduleWeek:
        # Get week schedule
        weekSchedule = cls.get_element('weekSchedule', id=WEEK_SCHEDULE_ID)
        
        week_days = {} 

        for index, day in enumerate(cls.days_keys):
            daily_schedule_id = weekSchedule.get(day, None)
            daily_schedule = cls.get_daily_schedule(daily_schedule_id) if daily_schedule_id else None
            
            openSpans: list[OpenSpan] = []
            if daily_schedule:
                week_days[day] = daily_schedule
            else: week_days[day] = None
           
        week_schedule = ScheduleWeek(**week_days)
        return week_schedule

    @classmethod
    def get_daily_schedule(cls, day_id: int) -> DailySchedule:
        if not day_id:
            return None

        daily_schedule = cls.get_element('dailySchedule', id=day_id)

        if daily_schedule and daily_schedule["openspans"]:
            openSpans: list[OpenSpan] = []
            
            for _open_span in cls.parse_open_spans(daily_schedule["openspans"]):
                openSpans.append(_open_span)

            return DailySchedule(daily_schedule["id"], openSpans)
        return None

    @classmethod
    def get_open_spans(cls, day_id: int) -> list[OpenSpan] | None:
        """
            Returns a list with all open spans from a certain day schedule or None if
            the daily schedule with "day_id" doesn't exists
        """
        if not day_id:
            return None

        schedule: DailySchedule = cls.get_daily_schedule(day_id)

        if schedule and schedule.openSpans:
            return schedule.openSpans
        
        return None

    @classmethod
    def remove_last_open_span(cls, day_id: int) -> DailySchedule| None:
        """
            Returns a list with all open spans from a certain day schedule or None if
            the daily schedule with "day_id" doesn't exists
        """
        if not day_id:
            return None

        query: str = f"""
            UPDATE dailySchedule
            SET openSpans = openSpans[1:array_length(openSpans, 1) - 1]
            WHERE id = %s;
        """
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            cursor.execute(query, (daily_schedule_id))
            rows_updated = cursor.rowcount
            
            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error creating open span: {e}")
            return None

        if rows_updated > 0:
            return True
        
        return False
    
    @classmethod
    def add_open_span(cls, daily_schedule_id, open_time: time, close_time: time) -> DailySchedule | None:
        
        if not daily_schedule_id or not open_time or not close_time:
            return None

        query = """
            UPDATE dailySchedule
            SET openSpans = ARRAY_APPEND(openSpans, (%s, %s)::OpenSpan)
            WHERE id = %s;
        """

        rows_updated: int

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            cursor.execute(query, (open_time, close_time, daily_schedule_id))
            rows_updated = cursor.rowcount
            
            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error creating open span: {e}")
            return None
        
        if rows_updated > 0:
            return cls.get_daily_schedule(daily_schedule_id)

        return None

    @classmethod
    def create_daily_schedule(cls) -> DailySchedule | None:
        insertQuery = "INSERT INTO dailySchedule DEFAULT VALUES RETURNING id;"
        result: DailySchedule = None
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(insertQuery)
            
            created_id = cursor.fetchone()['id']
            result = DailySchedule(created_id, [])
            # Apply chanages
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error creating daily schedule: {e}")

        return result

    @classmethod
    def update_week_schedule(cls, day_key: str, daily_schedule_id: int) -> bool:
        
        query = f"UPDATE weekSchedule SET {day_key} = %s WHERE id = %s"
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (daily_schedule_id, WEEK_SCHEDULE_ID))

            # Check the number of affected rows
            affected_rows = cursor.rowcount

            conn.commit()
            cursor.close()
            conn.close()
            
            # Checks whether any row has been updated
            if affected_rows == 0:
                return False
        except Exception as e:
            print(f"Error updating week schedule: {e}")
            return False

        return True

    @classmethod
    def remove_last_open_span(cls, daily_schedule_id: int) -> bool:

        print("SCHEDULE ID: ", daily_schedule_id)
        query = """
        UPDATE dailySchedule
            SET openSpans = CASE
                WHEN openSpans IS NULL THEN NULL
                WHEN array_length(openSpans, 1) > 1 THEN openSpans[1:array_length(openSpans, 1) - 1]
                ELSE NULL
            END
        WHERE id = %s;
        """

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(query, (daily_schedule_id,))
            affected_rows = cursor.rowcount

            conn.commit()

            cursor.close()
            conn.close()
            return affected_rows > 0

        except Exception as e:
            print(f"Error removing last open span: {e}")
            return False



    @classmethod
    def parse_open_spans(cls, openSpansString: str) -> OpenSpan:
        """Extract openSpans from database dailySchedule OpenSpans Array which is returned as string"""
        pattern = r'\((\d{2}:\d{2}:\d{2}),(\d{2}:\d{2}:\d{2})\)'
        matches = re.findall(pattern, openSpansString)
        
        openSpansList: list[OpenSpan] = []
        for _match in matches:
            openTimeStr = _match[0]
            endTimeStr = _match[1]

            # Convert strings to datetime.time objects
            open_time = datetime.strptime(openTimeStr, '%H:%M:%S').time()
            end_time = datetime.strptime(endTimeStr, '%H:%M:%S').time()
            openSpansList.append(OpenSpan(open_time, end_time))
        
        return openSpansList
        
