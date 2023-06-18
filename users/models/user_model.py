from enum import Enum
from users.entities.user import User, UserRole
from psycopg2 import connect, extras
from werkzeug.security import generate_password_hash, check_password_hash

from database.db_connection import get_connection


class UserModel:

    @classmethod
    def get_user(cls, id) -> User:
        result: dict
        try:
            
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            cursor.execute('SELECT * FROM users WHERE id = %s;', (id,))

            result = cursor.fetchone()
            
            if result != None:
                user_role: UserRole = UserRole.get_enum_value(result['role'])
                user: User = User(
                    id=result['id'], 
                    role=user_role, 
                    name=result['name'], 
                    email=result['email'], 
                    password=result['password'],
                    created_at=result['created_at']
                )
                return user
            
            conn.close()
        except Exception as e:
            print('An error occurred accessing the database')
            print(e)
            return None

        if result != None:
            user_role: UserRole = UserRole.get_enum_value(result['role'])
            user: User = User(
                id=result['id'], 
                role=user_role, 
                name=result['name'], 
                email=result['email'], 
                password=result['password'],
                created_at=result['created_at']
            )
            return user
        else:
            return None
    
    
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
            user_role: UserRole = UserRole.get_enum_value(result['role'])
            
            user: User = User(
                id=result['id'], 
                role=user_role, 
                name=result['name'], 
                email=result['email'], 
                password=result['password'],
                created_at=result['created_at']
            )
            
            return user
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
    def create_user(cls, role: str, name:str, email:str, password: str):
        # Pasword hashing for security purposes
        hashed_password = generate_password_hash(password)

        role = role.upper()

        result: dict
        
        try:
            # User is created on the database
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            query = 'INSERT INTO users(role, name, email, password) VALUES(%s, %s, %s, %s) RETURNING *'

            values = (role, name, email, hashed_password)

            cursor.execute(query, values)
            conn.commit()

            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
        except Exception as e:
            print('An error occurred accessing the database')
            print(e)
            return None


        if result != None:
            user_role: UserRole = UserRole.get_enum_value(result['role'])
            user: User = User(
                id=result['id'], 
                role=user_role, 
                name=result['name'], 
                email=result['email'], 
                password=result['password'],
                created_at=result['created_at']
            )
                
            return user
        else:
            return None



    @classmethod
    def update_user(cls, admin_user, updated_user):
        # Check if updater_user have enaugh privilegies to update
        if(admin_user.role != UserRole.ADMIN):
            raise Exception('Updater user have not got the needed privilegies to execute this action (Only admins can update users)')
        

    @classmethod
    def delete_user(cls, id):
        try:
            conn =  get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            cursor.execute('DELETE FROM users WHERE id = %s', (id,))

            conn.close()
        except Exception as e:
            return None
        

