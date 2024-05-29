import datetime
from services.users.entities.user import User
from services.tickets.entities.ticket import Ticket
from psycopg2 import extras

from services.users.models.user_model import UserModel
from services.zones.models.zone_model import ZoneModel
from services.zones.entities.zone import Zone
from services.utils.payment_methods import PaymentMethod


from database.db_connection import get_connection

from database.base_model import BaseModel



class TicketModel(BaseModel):

    @classmethod
    def get_ticket(cls, id:str) -> Ticket:
        """
            Returns a ticket object with the data saved on the database for the introduced id.
            Returns None if the ticket id doesn't exists
        """
        result = cls.get_element('tickets', id)

        responsible: User = UserModel.get_user(result["responsible_id"])
        zone: Zone = ZoneModel.get_zone(result["zone_id"])
        payment_method: PaymentMethod = PaymentMethod.get_enum_value(result["payment_method"])

        return Ticket(
            id = result["id"], 
            responsible = responsible,
            zone = zone,
            duration = result["duration"], 
            registration = result["registration"], 
            price = result["price"], 
            payment_method = payment_method, 
            created_at = result["created_at"]
        )
    

    @classmethod
    def get_tickets(cls, interval: tuple = None, **kwargs) -> list[dict]:
        
        result = cls.get_elements('tickets', interval, **kwargs)

        tickets: list[Ticket] = []

        for ticket in result:
            # Creating ticket object from database ticket data
            responsible: User = UserModel.get_user(ticket["responsible_id"])
                
            zone: Zone = ZoneModel.get_zone(ticket["zone_id"])
            payment_method: PaymentMethod = PaymentMethod.get_enum_value(ticket["payment_method"])

            tickets.append(
                Ticket(
                    id = ticket["id"], 
                    responsible = responsible,
                    zone = zone,
                    duration = ticket["duration"], 
                    registration = ticket["registration"], 
                    price = ticket["price"], 
                    payment_method = payment_method, 
                    created_at = ticket["created_at"]
                ).to_json()
            )
        
        return tickets



    @classmethod
    def delete_tickets(cls, **kwargs) -> list[dict]:
        
        result = cls.delete_tickets('tickets', **kwargs)

        tickets: list[Ticket] = []

        for ticket in result:
            # Creating ticket object from database ticket data
            responsible: User = UserModel.get_user(ticket["responsible_id"])
                
            zone: Zone = ZoneModel.get_zone(ticket["zone_id"])
            payment_method: PaymentMethod = PaymentMethod.get_enum_value(ticket["payment_method"])

            tickets.append(
                Ticket(
                    id = ticket["id"], 
                    responsible = responsible,
                    zone = zone,
                    duration = ticket["duration"], 
                    registration = ticket["registration"], 
                    price = ticket["price"], 
                    payment_method = payment_method, 
                    created_at = ticket["created_at"]
                ).to_json()
            )
        
        return tickets
    

    @classmethod
    def count_tickets(cls, **kwargs) -> int:
        return cls.count_elements('tickets', **kwargs)
    

    @classmethod
    def create_ticket(cls, 
                responsible: User, 
                zone: Zone,
                duration: str, 
                registration:str, 
                price: float, 
                payment_method: PaymentMethod,
                created_at: datetime.datetime
            ) -> Ticket:
        
        """Returns the created Ticket if is successfully created."""

        ticket: Ticket
        zone_tickets_amount = ZoneModel.count_ticket(zone.id)

        if(zone_tickets_amount < 0):
            return None
    
        id = f"{zone.identifier}/{str(zone_tickets_amount).zfill(5)}"

        query = '''
                INSERT INTO tickets(id, responsible_id, zone_id, duration, registration, price, payment_method, created_at) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING *
            '''
        
        values = (id, responsible.id, zone.id, duration, registration, price, payment_method.value, created_at)

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            cursor.execute(query, values)
            
            result = cursor.fetchone()

            # Creating ticket object from database ticket data
            payment_method: PaymentMethod = PaymentMethod.get_enum_value(result["payment_method"])

            ticket = Ticket(
                id = result["id"], 
                responsible = responsible,
                zone = zone,
                duration = result["duration"], 
                registration = result["registration"], 
                price = result["price"], 
                payment_method = payment_method, 
                created_at = result["created_at"])
            
            conn.commit()
            conn.close()

        except Exception as exception:
            print("create_ticket: ", exception)
            return None
        
        return ticket
    

    @classmethod
    def delete_ticket(cls, id: str) -> Ticket:
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
            print("delete_ticket: ", exception)
            return None

        return deleted_ticket

