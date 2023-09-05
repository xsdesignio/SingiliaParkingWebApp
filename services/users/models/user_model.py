
from psycopg2 import extras
from werkzeug.security import generate_password_hash, check_password_hash

from database.db_connection import get_connection
from ..entities.user import User, UserRole
from services.zones.entities.zone import Zone
from services.zones.models.zone_model import ZoneModel

class UserModel:

    @classmethod
    def get_user(cls, id) -> User:
        result: dict
        try:
            
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            cursor.execute('SELECT * FROM users WHERE id = %s;', (id,))

            result = cursor.fetchone()
            
            conn.close()
        except Exception as e:
            print('An error occurred accessing the database')
            print(e)
            return None

        return cls.create_user_from_result(result)

    
    @classmethod
    def get_validated_user(cls, email, password) -> User:
        result: dict

        try:
            conn =  get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM users WHERE email=%s;', (email,))
            result = cursor.fetchone()

            conn.close()

        except Exception as e:
            print('An error occurred accessing the database')
            print(e)
            return None
        

        if result != None and check_password_hash(result['password'], password):
            return cls.create_user_from_result(result)
        else:
            return None
        
    
    # This method doesn't return the User class for the objects to improve eficiency
    # I am supossing that listing multiple users is just for informational purposes 
    # so instantiate a User class for every result is not useful (and do increase considerably the time of execution when the users database grows)
    @classmethod
    def get_users_list(cls):
        results: list(dict)
        try:
            conn =  get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute('SELECT * FROM users')
            results = cursor.fetchall()
            conn.close()
        except Exception as e:
            print('An error occurred accessing the database')
            print(e)
            return None

        return results


    @classmethod
    def create_user(cls, role: str, name:str, email:str, password: str, associated_zone: Zone = None):
        # Pasword hashing for security purposes
        hashed_password = generate_password_hash(password)

        role = role.upper()

        result: dict
        
        try:
            # User is created on the database
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            query = 'INSERT INTO users(role, name, email, password'

            values = [role, name, email, hashed_password]

            if associated_zone != None:
                query += ', associated_zone_id) VALUES(%s, %s, %s, %s, %s) RETURNING *'
                values.append(associated_zone.id)
            else:
                query += ') VALUES(%s, %s, %s, %s) RETURNING *'

            cursor.execute(query, values)
            conn.commit()

            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
        except Exception as e:
            print('An error occurred accessing the database')
            print(e)
            return None

        return cls.create_user_from_result(result)


    @classmethod
    def update_user(cls, user_id, new_user_data: dict) -> User:
        result: dict

        try:
            conn =  get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            cursor.execute('UPDATE users SET role = %s, name = %s, email = %s WHERE id = %s RETURNING *', (new_user_data['role'], new_user_data['name'], new_user_data['email'], user_id))

            result = cursor.fetchone()
            
            conn.commit()
            conn.close()
        except Exception as e:
            return None

        return cls.create_user_from_result(result)
        

    @classmethod
    def delete_user(cls, id):
        result: dict

        try:
            conn =  get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            cursor.execute('DELETE FROM users WHERE id = %s RETURNING *', (id,))

            result = cursor.fetchone()
            
            conn.commit()
            conn.close()
        except Exception as e:
            return None
        
        return cls.create_user_from_result(result)
        
    @classmethod
    def asign_zone_to_user(cls, user_id, zone: Zone) -> bool:
        
        if zone == None:
            return False
        
        try:
            conn =  get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            cursor.execute('UPDATE users SET associated_zone_id = %s WHERE id = %s', (zone.id, user_id))

            conn.commit()
            conn.close()
        except Exception as e:
            print('An error occurred accessing the database')
            print(e)
            return False
        
        return True


    def create_user_from_result(result) -> User:
        if result == None:
            return None
        
        user_role: UserRole = UserRole.get_enum_value(result['role'])
        associated_zone_id = result.get('associated_zone_id')
        associated_zone: Zone = None

        if associated_zone_id != None:
            associated_zone = ZoneModel.get_zone(associated_zone_id)

        user: User = User(
            id=result['id'], 
            role=user_role, 
            name=result['name'], 
            email=result['email'], 
            associated_zone=associated_zone,
            password=result['password'],
            created_at=result['created_at']
        )
        return user