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
            print("get_zones_list: ", exception)
            return None
        return result
    
    @classmethod
    def get_zone_by_name(cls, name) -> Zone:
        zone: Zone
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM zones WHERE name = %s', (name,))
            result = cursor.fetchone()
            
            if result is None:
                return None
            
            zone = Zone(result["id"], result["name"])

            conn.close()
        except Exception as exception:
            print("get_zone_by_name: ", exception)
            return None
        return zone
    
    @classmethod
    def get_zone(cls, id) -> Zone:
        zone: Zone
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM zones WHERE id = %s', (id,))
            result = cursor.fetchone()

            zone = Zone(result["id"], result["name"])

            conn.close()
        except Exception as exception:
            print("get_zone: ", exception)
            return None
        return zone
    
    @classmethod
    def create_zone(cls, name) -> bool:
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('INSERT INTO zones (name) VALUES (%s) RETURNING *', (name,))
            
            result = cursor.fetchone()

            zone = Zone(result["id"], result["name"])
            
            conn.commit()
            conn.close()

            return zone
        
        except Exception as exception:

            print("create_zone: ", exception)

            return None
    
    @classmethod
    def delete_zone(cls, id) -> bool:
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute('UPDATE tickets SET zone_id = NULL WHERE zone_id = %s', (id,))
            cursor.execute('UPDATE bulletins SET zone_id = NULL WHERE zone_id = %s', (id,))
            cursor.execute('UPDATE users SET associated_zone_id = NULL WHERE associated_zone_id = %s', (id,))

            cursor.execute('DELETE FROM zones WHERE id = %s', (id,))
            conn.commit()
            conn.close()
        except Exception as exception:
            print("delete_zone: ", exception)
            return False
        return True
    
    @classmethod
    def update_zone(cls, id, new_name) -> bool:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE zones SET name = %s WHERE id = %s', (new_name, id))
            conn.commit()
            conn.close()
        except Exception as exception:
            print("update_zone: ", exception)
            return False
        return True