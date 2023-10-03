from psycopg2 import extras

from ..entities.available_ticket import AvailableTicket


from database.db_connection import get_connection

from database.base_model import BaseModel


class AvailableTicketModel(BaseModel):

    @classmethod
    def get_available_ticket(cls, id) -> AvailableTicket:
        """
            Returns an AvailableTicket object with params id.
            Returns an exception if it is not found.
        """
        available_bulletin: AvailableTicket
        db_result = cls.get_element('available_tickets', id)

        if db_result == None:
            return None
        
        available_ticket = AvailableTicket.from_dict(db_result)
        return available_ticket

    @classmethod
    def get_available_tickets(cls) -> list[dict]:
        """
            Returns a list of available tickets
        """
        db_results = cls.get_elements('available_tickets')
        print("db_results", db_results)
        available_tickets: list[AvailableTicket] = []

        for result in db_results:
            available_ticket: AvailableTicket = AvailableTicket.from_dict(result)
            available_tickets.append(available_ticket.to_json())
        
        print("available_tickets: ", available_tickets)
        return available_tickets
    
    @classmethod
    def create_available_ticket(cls, ticket_duration: str, ticket_price: float) -> AvailableTicket:
        """
            Creates a new ticket and returns it
        """
        available_ticket: AvailableTicket

        query = '''
                INSERT INTO available_tickets(duration, price) 
                VALUES(%s, %s) 
                RETURNING *
            '''
        values = (ticket_duration, ticket_price)

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            cursor.execute(query, values)
            
            result = cursor.fetchone()

            # Creating available_ticket object from database ticket data
            available_ticket = AvailableTicket.from_dict(result)

            conn.commit()
            conn.close()

        except Exception as e:
            print("create_available_ticket: ", e)
            return None
        
        return available_ticket.to_json()
    

    @classmethod
    def edit_available_ticket(cls, id: id, duration: str, price: int):
        """
            Edit the available_ticket with params id and returns it.
            Returns an exception if it is not found.
        """
        available_ticket: AvailableTicket

        query = '''
                UPDATE available_tickets
                SET duration = %s, price = %s
                WHERE id = %s
                RETURNING *
            '''
        values = (duration, price, id)

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            cursor.execute(query, values)
            
            result = cursor.fetchone()

            # Creating available_ticket object from database ticket data
            available_ticket = AvailableTicket.from_dict(result)

            conn.commit()
            conn.close()

        except Exception as e:
            print("edit_available_ticket: ", e)
            return None
        
        return available_ticket.to_json()

    @classmethod
    def delete_available_ticket(cls, id: int) -> bool:
        """
            Delete the available_ticket with params id and returns it.
            Returns an exception if it is not found.
        """
        return cls.delete_element('available_tickets', id)
