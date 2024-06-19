from psycopg2 import extras
from ..entities.available_bulletin import AvailableBulletin
from database.db_connection import get_connection
from decimal import Decimal
from database.base_model import BaseModel




class AvailableBulletinModel(BaseModel):
    
    @classmethod
    def get_available_bulletin(cls, id) -> AvailableBulletin:
        """
            Returns the available_bulletin with params id.
            Returns an exception if it is not found.
        """
        available_bulletin: AvailableBulletin
        db_result = cls.get_element('available_bulletins', id)

        if db_result == None:
            return None
        
        available_bulletin = AvailableBulletin.from_dict(db_result)
        return available_bulletin
    

    @classmethod
    def get_available_bulletins(cls) -> list[dict]:
        """
            Returns a list of available bulletins
        """
        db_results = cls.get_elements('available_bulletins')
        
        available_bulletins: list[AvailableBulletin] = []

        for result in db_results:
            available_bulletin: AvailableBulletin = AvailableBulletin.from_dict(result)
            available_bulletins.append(available_bulletin.to_json())
        
        # Order result by duration minutes in ascending order
        sorted_list: list = sorted(available_bulletins, key = lambda bulletin: bulletin['duration_minutes'])
        
        return sorted_list
    
    
    @classmethod
    def create_available_bulletin(cls, bulletin_duration: str, bulletin_duration_minutes: int, bulletin_price: float) -> AvailableBulletin:
        """
            Creates a new bulletin and returns it
        """
        available_bulletin: AvailableBulletin

        query = '''
                INSERT INTO available_bulletins(duration, duration_minutes, price) 
                VALUES(%s, %s, %s) 
                RETURNING *
            '''
        values = (bulletin_duration, bulletin_duration_minutes, bulletin_price)

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            cursor.execute(query, values)
            
            result = cursor.fetchone()

            # Creating available_bulletin object from database bulletin data
            available_bulletin = AvailableBulletin.from_dict(result)

            conn.commit()
            conn.close()

        except Exception as e:
            print("create_available_bulletin: ", e)
            return None
        
        return available_bulletin.to_json()
    

    @classmethod
    def edit_available_bulletin(cls, id: id, duration: str, duration_minutes: int, price: float | Decimal):
        """
            Edit the available_bulletin with params id and returns it.
            Returns an exception if it is not found.
        """
        available_bulletin: AvailableBulletin

        query = '''
                UPDATE available_bulletins
                SET duration = %s, duration_minutes = %s,price = %s
                WHERE id = %s
                RETURNING *
            '''
        values = (duration, duration_minutes, price, id)

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            cursor.execute(query, values)
            
            result = cursor.fetchone()

            # Creating available_bulletin object from database bulletin data
            available_bulletin = AvailableBulletin.from_dict(result)

            conn.commit()
            conn.close()

        except Exception as e:
            print("edit_available_ticket: ", e)
            return None
        
        return available_bulletin.to_json()

    @classmethod
    def delete_available_bulletin(cls, id: int) -> bool:
        """
            Delete the available_bulletin with params id and returns it.
            Returns an exception if it is not found.
        """
        return cls.delete_element('available_bulletins', id)
