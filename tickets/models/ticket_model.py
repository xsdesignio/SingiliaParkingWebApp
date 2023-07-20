import datetime
from users.entities.user import User
from tickets.entities.ticket import Ticket
from psycopg2 import extras

from users.models.user_model import UserModel

from database.db_connection import get_connection



class TicketModel:
    @classmethod
    def get_tickets(cls) -> list[dict]:
        result: list[dict]
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM tickets')
            result = cursor.fetchall()
            conn.close()
        except Exception as exception:
            return None
        return result
    
    @classmethod
    def get_tickets_by_filter(cls, start_date: datetime.datetime = None, end_date: datetime.datetime = None, location: str = None) -> list[dict]:
        result: list[dict]
        
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            # Build the SQL query dynamically based on the provided parameters
            query = 'SELECT * FROM tickets WHERE created_at BETWEEN %s AND %s'
            params = [start_date, end_date]

            if location:
                query += ' AND location = %s'
                params.append(location)

            cursor.execute(query, params)
            result = cursor.fetchall()
            conn.close()
        except Exception as exception:
            return None
        return result
    

    @classmethod
    def count_all_tickets_variables_by_filter(cls, start_date: datetime.datetime = None, end_date: datetime.datetime = None, location: str = None):
        """Return a dictionary with the variables and their count"""
        paid_by_card = cls.count_tickets_variable_by_filter(start_date, end_date, location, 'paid', True)
        paid_by_cash = cls.count_tickets_variable_by_filter(start_date, end_date, location, 'paid', False)
        duration_of_30 = cls.count_tickets_variable_by_filter(start_date, end_date, location, 'duration', 30)
        duration_of_60 = cls.count_tickets_variable_by_filter(start_date, end_date, location, 'duration', 60)
        duration_of_90 = cls.count_tickets_variable_by_filter(start_date, end_date, location, 'duration', 90)
        duration_of_120 = cls.count_tickets_variable_by_filter(start_date, end_date, location, 'duration', 120)

        tickets_amount_by_data = {
            "paid_by_card": paid_by_card,
            "paid_by_cash": paid_by_cash,
            "duration_of_30": duration_of_30,
            "duration_of_60": duration_of_60,
            "duration_of_90": duration_of_90,
            "duration_of_120": duration_of_120,
        }

        return tickets_amount_by_data
    

    @classmethod
    def count_tickets_variable_by_filter(cls, start_date: datetime.datetime = None, end_date: datetime.datetime = None, location: str = None, variable: str = None, value = None):
        count: int
        
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            # Build the SQL query dynamically based on the provided parameters
            query = 'SELECT COUNT(*) AS count FROM tickets WHERE created_at BETWEEN %s AND %s'
            
            params = [start_date, end_date]
            if location:
                query += ' AND location = %s'
                params.append(location)
            
            query += f' AND {variable} = %s'

            params.append(value)

            
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            count = result["count"]

            conn.close()
            
        except Exception as exception:
            return None
        return count


    @classmethod
    def get_ticket(cls, id:int) -> Ticket:
        """
            Returns a ticket object with the data saved on the database for the introduced id.
            Returns None if the ticket id doesn't exists
        """
        ticket: Ticket
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM tickets WHERE id= %s', (id,))

            result = cursor.fetchone()

            # Creating ticket object from database ticket data
            responsible: User = UserModel.get_user(result["responsible_id"])
            
            
            ticket: Ticket = Ticket(
                result["id"], 
                responsible, 
                result["duration"], 
                result["price"], 
                result["registration"], 
                result["paid"], 
                result["location"], 
                result["created_at"])
            
            conn.close()
        except Exception as exception:
            print(exception)
            return None
        
        return ticket
    

    @classmethod
    def create_ticket(cls, 
                      responsible_id: int, 
                      duration: int, 
                      registration:str, 
                      price: float, 
                      paid: bool,
                      location: str,
                      created_at: datetime.datetime) -> Ticket:
        
        """Returns the created Ticket if is successfully created."""

        ticket: Ticket

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            query = '''
                INSERT INTO tickets(responsible_id, duration, registration, price, paid, location, created_at) 
                VALUES(%s, %s, %s, %s, %s, %s, %s ) 
                RETURNING *
            '''

            values = (responsible_id, duration, registration, price, paid, location, created_at)
            
            cursor.execute(query, values)

            
            result = cursor.fetchone()

            # Creating ticket object from database ticket data
            responsible: User = UserModel.get_user(responsible_id)
            
            ticket: Ticket = Ticket(
                result["id"], 
                responsible, 
                result["duration"], 
                result["price"], 
                result["registration"], 
                result["paid"], 
                result["location"], 
                result["created_at"])
            
            conn.commit()
            
            conn.close()

        except Exception as exception:
            print(exception)
            return None
        
        return ticket
    

    @classmethod
    def delete_ticket(cls, id: int) -> Ticket:
        """
            Delete the ticket with params id and returns it.
            Returns an exception if it is not found.
        """

        deleted_ticket:Ticket = cls.get_ticket(id)
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            cursor.execute('DELETE FROM tickets WHERE id = %s', (id,))
            conn.commit()
            conn.close()
        except Exception as exception:
            print(exception)
            return None

        return deleted_ticket


    @classmethod
    def pay_ticket(cls, ticket_id: int) -> Ticket:
        updated_ticket: Ticket

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            ticket: Ticket = cls.get_ticket(ticket_id)

            if ticket.paid:
                raise Exception("El ticket introducido ya ha sido pagado")

            query = '''
                UPDATE tickets SET paid = true
                WHERE id = %s
                RETURNING *
            '''


            cursor.execute(query, (ticket_id,))
            result = cursor.fetchone()

            # Creating ticket object from database ticket data
            responsible = UserModel.get_user(result["responsible_id"])

                
            updated_ticket = Ticket(
                result["id"], 
                responsible, 
                result["duration"], 
                result["price"], 
                result["registration"], 
                result["paid"], 
                result["location"],
                result["created_at"])

            conn.commit()
                
            conn.close()
            

            return updated_ticket
        
        except Exception as exception:
            print(exception)
            return None



    
