import datetime
from users.entities.user import User
from ..entities.bulletin import Bulletin
from psycopg2 import extras

from users.models.user_model import UserModel

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
            
            bulletin: bulletin = Bulletin(
                result["id"],
                responsible, 
                result["location"], 
                result["registration"], 
                result["duration"], 
                result["price"], 
                result["paid"], 
                result["brand"], 
                result["model"], 
                result["signature"], 
                result["created_at"])
            conn.close()
        except Exception as exception:
            return None
        
        return bulletin
    

    @classmethod
    def create_bulletin(self, 
                 responsible_id: int, 
                 location: str,
                 registration: str,
                 duration: int,
                 price: float,
                 paid: bool,
                 brand: str,
                 model: str,
                 signature: str,
                 created_at:datetime.datetime) -> Bulletin:
        
        """Returns the created Bulletin if is successfully created."""

        bulletin: Bulletin

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            query = '''
                INSERT INTO bulletins(responsible_id, location, registration, duration,
                    price, paid, brand, model, signature, created_at) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING *
            '''

            values = (responsible_id, location, registration, duration, price, paid, brand, model, signature, created_at)
            
            cursor.execute(query, values)

            
            result = cursor.fetchone()

            # Creating bulletin object from database bulletin data
            responsible: User = UserModel.get_user(responsible_id)

            bulletin: bulletin = Bulletin(
                result["id"],
                responsible, 
                result["location"], 
                result["registration"], 
                result["duration"], 
                result["price"], 
                result["paid"], 
                result["brand"], 
                result["model"], 
                result["signature"], 
                result["created_at"])

            
            conn.commit()
            cursor.close()
            conn.close()

        except Exception as exception:
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
        updated_bulletin = Bulletin(
            result["id"],
            responsible, 
            result["location"], 
            result["registration"], 
            result["duration"], 
            result["price"], 
            result["paid"], 
            result["brand"], 
            result["model"], 
            result["signature"], 
            result["created_at"])
        conn.commit()
        cursor.close()
        conn.close()

        
        
        return updated_bulletin
        



    
