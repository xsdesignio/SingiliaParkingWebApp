from psycopg2 import connect, extras
from tickets.entities.zone import Zone

from database.db_connection import get_connection



class ZoneModel:
    def get_zones():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute('SELECT * FROM users')
        zones = cursor.fetchall()
        conn.close()
        return zones

    def get_zone(id: int) -> Zone:
        zone: Zone
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM zones WHERE id = %s', (id,))
            result = cursor.fetchone()
            zone = Zone(result['id'], result['name'], result['created_at'])
            conn.close()
        except:
            return None

        return zone
        
    
    def create_zone(name) -> Zone:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute('INSERT INTO zones(name) VALUES(%s) RETURNING *', (name,))
        result = cursor.fetchall()
        zone:Zone = Zone(result['id'], result['name'], result['created_at'])
        conn.close()
        return zone
    

    def delete_zone(id):
        pass
