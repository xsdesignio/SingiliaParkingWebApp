from psycopg2 import extras
from database.db_connection import get_connection

from services.zones.entities.zone import Zone


class ZoneModel:
    
    @classmethod
    def get_zones_list(cls) -> list[Zone]:
        result: list[Zone]
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM zones')
            result = cursor.fetchall()
            conn.close()
        except Exception as exception:
            print(exception)
            return None
        return result
    
    @classmethod
    def get_zone_by_name(cls, name) -> Zone:
        result: Zone
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM zones WHERE name = %s', (name))
            result = cursor.fetchone()
            conn.close()
        except Exception as exception:
            print(exception)
            return None
        return result
    
    @classmethod
    def get_zone(cls, id) -> Zone:
        result: Zone
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM zones WHERE id = %s', (id))
            result = cursor.fetchone()
            conn.close()
        except Exception as exception:
            print(exception)
            return None
        return result
    
    @classmethod
    def create_zone(cls, name) -> bool:
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('INSERT INTO zones (name) VALUES (%s) RETURNING *', (name, ))
            
            result = cursor.fetchone()

            zone = Zone(result["id"], result["name"])
            
            conn.commit()
            conn.close()

            return zone
        
        except Exception as exception:

            print(f"Exception: {exception}")

            return None
    
    @classmethod
    def delete_zone(cls, id) -> bool:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM zones WHERE id = %s', (id))
            conn.commit()
            conn.close()
        except Exception as exception:
            print(exception)
            return False
        return True