import datetime
from entities.user import User
from entities.ticket import Ticket
from entities.zone import Zone
from psycopg2 import connect, extras

from .db_connection import get_connection

class TicketModel:
    @classmethod
    def get_tickets(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tickets;')
        result = cursor.fetchall()
        print(result)
        conn.close()
        return result

    @classmethod
    def get_ticket(cls, id:int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT ticket FROM tickets WHERE id= %s RETURNING;', (id,))
        result = cursor.fetchone()
        print(result)
        conn.close()

        return result

    #Returns the created Ticket if is successfully created
    @classmethod
    def create_ticket(cls, author:User, zone: Zone):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

        query = 'INSERT INTO tickets(responsible_id, zone_id) VALUES(%s, %s) RETURNING *'


        values = (author, zone)

        cursor.execute(query, values)
        conn.commit()

        result = cursor.fetchone()
        
        cursor.close()
        conn.close()

        return result


    
