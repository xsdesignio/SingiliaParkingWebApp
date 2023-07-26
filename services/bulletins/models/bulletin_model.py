import datetime
from services.users.entities.user import User
from ..entities.bulletin import Bulletin
from psycopg2 import extras

from services.users.models.user_model import UserModel
from services.zones.models.zone_model import ZoneModel
from services.zones.entities.zone import Zone
from services.utils.payment_methods import PaymentMethod

from database.db_connection import get_connection

class BulletinModel:
    @classmethod
    def get_bulletins(cls) -> list[dict]:
        result: list[dict]
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM bulletins')
            result = cursor.fetchall()
            conn.close()
        except Exception as exception:
            return None
        return result


    @classmethod
    def get_bulletin(cls, id:int) -> Bulletin:
        """
            Returns a bulletin object with the data saved on the database for the introduced id.
            Returns None if the bulletin id doesn't exists
        """
        bulletin: Bulletin

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM bulletins WHERE id= %s', (id,))

            result = cursor.fetchone()

            # Creating bulletins object from database bulletins data
            responsible: User = UserModel.get_user(result["responsible_id"])
            zone: Zone = ZoneModel.get_zone(result["zone_id"])
            payment_method: PaymentMethod = PaymentMethod(result["payment_method"])
            
            bulletin: bulletin = Bulletin(
                id = result["id"],
                responsible = responsible, 
                zone = zone, 
                duration = result["duration"], 
                registration = result["registration"], 
                price = result["price"], 
                payment_method= payment_method,
                paid = result["paid"], 
                created_a = result["created_at"],
                brand = result.get("brand"), 
                model = result.get("model"), 
                color = result.get("color") 
            )

            conn.close()

        except Exception as exception:
            return None
        
        return bulletin
    

    @classmethod
    def get_bulletins_by_filter(cls, start_date: datetime.datetime = None, end_date: datetime.datetime = None, zone: Zone = None) -> list[dict]:
        result: list[dict]
        
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            # Build the SQL query dynamically based on the provided parameters
            query = 'SELECT * FROM bulletins WHERE created_at BETWEEN %s AND %s'
            params = [start_date, end_date]

            if zone:
                query += ' AND zone_id = %s'
                params.append(zone.id)
            

            cursor.execute(query, params)
            result = cursor.fetchall()
            conn.close()
            
        except Exception as exception:
            return None
        return result
    
    
    @classmethod
    def count_bulletins_by_attribute(cls, attribute: str, value, start_date: datetime.datetime = None, end_date: datetime.datetime = None, zone: Zone = None):
        count: int
        
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            # Build the SQL query dynamically based on the provided parameters
            query = 'SELECT COUNT(*) AS count FROM bulletins WHERE created_at BETWEEN %s AND %s'
            
            params = [start_date, end_date]
            if zone:
                query += ' AND zone_id = %s'
                params.append(zone.id)
            
            query += f' AND {attribute} = %s'

            params.append(value)

            
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            count = result["count"]

            conn.close()
            
        except Exception as exception:
            return None
        
        return count
    

    @classmethod
    def create_bulletin(self, 
                responsible: User, 
                zone: Zone,
                duration: int,
                registration: str,
                price: float,
                payment_method: PaymentMethod,
                paid: bool,
                created_at:datetime.datetime = datetime.datetime.now(),
                brand: str = None,
                model: str = None,
                color: str = None
            ) -> Bulletin:
        
        """Returns the created Bulletin if is successfully created."""

        bulletin: Bulletin

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            query = '''
                INSERT INTO bulletins(responsible_id, zone_id, duration, registration,
                    price, payment_method_id, paid, brand, model, color, created_at) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING *
            '''

            values = (responsible.id, zone.id, duration, registration, price, payment_method.value, paid, brand, model, color, created_at)
            
            cursor.execute(query, values)

            
            result = cursor.fetchone()

            # Creating bulletin object from database bulletin data
            payment_method: PaymentMethod = PaymentMethod(result["payment_method"])


            bulletin: bulletin = Bulletin(
                id = result["id"],
                responsible = responsible, 
                zone = zone, 
                duration = result["duration"], 
                registration = result["registration"], 
                price = result["price"], 
                payment_method= payment_method.value,
                paid = result["paid"], 
                created_a = result["created_at"],
                brand = result.get("brand"), 
                model = result.get("model"), 
                color = result.get("color") 
            )

            
            conn.commit()
            cursor.close()
            conn.close()

        except Exception as exception:
            print(exception)
            return None
        
        return bulletin
    

    @classmethod
    def delete_bulletin(cls, id: int) -> Bulletin:
        """
            Delete the bulletin with params id and returns it.
            Returns an exception if it is not found.
        """

        deleted_bulletin:Bulletin = cls.get_bulletin(id)
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            cursor.execute('DELETE FROM bulletins WHERE id = %s', (id,))
            conn.commit()
            conn.close()
        except Exception as exception:
            return None

        return deleted_bulletin


    @classmethod
    def pay_bulletin(cls, bulletin_id:int) -> Bulletin:
        updated_bulletin: Bulletin
        
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)


        bulletin: Bulletin = cls.get_bulletin(bulletin_id)

        if bulletin.paid:
            raise Exception("El boletín introducido ya ha sido pagado")


        query = '''
            UPDATE bulletins SET paid = true
            WHERE id = %s
            RETURNING *
        '''

        cursor.execute(query, (bulletin_id, ))
        result = cursor.fetchone()

        # Creating bulletin object from database bulletin data
        responsible: User = UserModel.get_user(result["responsible_id"])
        zone: Zone = ZoneModel.get_zone(result["zone_id"])
        payment_method: PaymentMethod = PaymentMethod(result["payment_method"])


        bulletin: updated_bulletin = Bulletin(
            id = result["id"],
            responsible = responsible, 
            zone = zone, 
            duration = result["duration"], 
            registration = result["registration"], 
            price = result["price"], 
            payment_method= payment_method,
            paid = result["paid"], 
            created_a = result["created_at"],
            brand = result.get("brand"), 
            model = result.get("model"), 
            color = result.get("color") 
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        return updated_bulletin
        



    
