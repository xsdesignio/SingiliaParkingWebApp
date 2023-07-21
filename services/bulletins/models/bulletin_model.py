import datetime
from services.users.entities.user import User
from ..entities.bulletin import Bulletin
from psycopg2 import extras

from services.users.models.user_model import UserModel

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
                result["created_at"],
                result.get("brand"), 
                result.get("model"), 
                result.get("color") 
            )

            conn.close()

        except Exception as exception:
            return None
        
        return bulletin
    


    @classmethod
    def get_bulletins_by_filter(cls, start_date: datetime.datetime = None, end_date: datetime.datetime = None, location: str = None) -> list[dict]:
        result: list[dict]
        
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            # Build the SQL query dynamically based on the provided parameters
            query = 'SELECT * FROM bulletins WHERE created_at BETWEEN %s AND %s'
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
    def count_all_bulletins_variables_by_filter(cls, start_date: datetime.datetime = None, end_date: datetime.datetime = None, location: str = None):
        """Return a dictionary with the variables and their count"""

        paid_by_card = cls.count_bulletins_variable_by_filter(start_date, end_date, location, 'paid', True)
        paid_by_cash = cls.count_bulletins_variable_by_filter(start_date, end_date, location, 'paid', False)
        duration_of_30 = cls.count_bulletins_variable_by_filter(start_date, end_date, location, 'duration', 30)
        duration_of_60 = cls.count_bulletins_variable_by_filter(start_date, end_date, location, 'duration', 60)
        duration_of_90 = cls.count_bulletins_variable_by_filter(start_date, end_date, location, 'duration', 90)
        duration_of_120 = cls.count_bulletins_variable_by_filter(start_date, end_date, location, 'duration', 120)

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
    def count_bulletins_variable_by_filter(cls, start_date: datetime.datetime = None, end_date: datetime.datetime = None, location: str = None, variable: str = None, value = None):
        count: int
        
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            # Build the SQL query dynamically based on the provided parameters
            query = 'SELECT COUNT(*) AS count FROM bulletins WHERE created_at BETWEEN %s AND %s'
            
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
    def create_bulletin(self, 
                responsible_id: int, 
                location: str,
                registration: str,
                duration: int,
                price: float,
                paid: bool,
                created_at:datetime.datetime,
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
                INSERT INTO bulletins(responsible_id, location, registration, duration,
                    price, paid, brand, model, color, created_at) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING *
            '''

            values = (responsible_id, location, registration, duration, price, paid, brand, model, color, created_at)
            
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
                result["created_at"],
                result.get("brand"), 
                result.get("model"), 
                result.get("color")
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
        updated_bulletin = Bulletin(
            result["id"],
            responsible, 
            result["location"], 
            result["registration"], 
            result["duration"], 
            result["price"], 
            result["paid"], 
            result["created_at"],
            result.get("brand"), 
            result.get("model"), 
            result.get("color"), 
        )
        conn.commit()
        cursor.close()
        conn.close()

        
        
        return updated_bulletin
        



    
