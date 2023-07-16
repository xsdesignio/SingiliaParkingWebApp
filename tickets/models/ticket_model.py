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



    
