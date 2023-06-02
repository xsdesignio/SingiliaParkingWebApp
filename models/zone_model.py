from psycopg2 import connect, extras
from entities.zone import Zone

from .db_connection import get_connection



class ZoneModel:
    def get_zones():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute('SELECT * FROM users')
        zones = cursor.fetchall()
        conn.close()
        return zones

    def get_zone(id: int) -> Zone:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s RETURNING *', (id,))
        result = cursor.fetchall()
        zone:Zone = Zone(result['id'], result['name'], result['created_at'])
        conn.close()
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
