from datetime import timedelta
from .db_connection import get_connection
from psycopg2 import extras



class BaseModel:
    @classmethod
    def get_element(cls, table, id):
        result: dict
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(f'SELECT * FROM { table } WHERE id= %s', (id,))

            result = cursor.fetchone()

            conn.close()
        except Exception as exception:
            print("get_element: ", exception)
            return None
        
        return result

    @classmethod
    def get_elements(cls, table, **kwargs) -> list[dict]:
        query = f'SELECT * FROM { table }'
        params = []

        dict_size = len(kwargs)
        current_index = 0

        # Build the SQL query dynamically based on the provided parameters
        if dict_size > 0:

            query += ' WHERE '

            for key, value in kwargs.items():
                    
                if key == 'start_date':
                    query += f'created_at >= %s'
                    value -= timedelta(days=1)
                elif key == 'end_date':
                    query += f'created_at <= %s'
                    value+= timedelta(days=1)
                else:
                    query += f'{key} = %s'

                params.append(value)

                if current_index < (dict_size - 1):
                    query += ' AND '
                    
                current_index += 1

        # Execute the query
        result: list[dict]
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            cursor.execute(query, params)
            result = cursor.fetchall()
                
            conn.close()
        except Exception as exception:
            print("get_elements: ", exception)
            return None
        
        return result
    
    @classmethod
    def count_elements(cls, table, **kwargs) -> int:
        count: int
        
        query = f'SELECT COUNT(*) AS count FROM { table }'
        params = []

        # Build the SQL query dynamically based on the provided parameters
        # Add querired parameters to the params list
        dict_size = len(kwargs)
        current_index = 0
        if dict_size > 0:

            query += ' WHERE '

            for key, value in kwargs.items():
                    
                if key == 'start_date':
                    query += 'created_at > %s'
                    value_copy = value - timedelta(days=1)
                    params.append(value_copy)
                elif key == 'end_date':
                    query += 'created_at < %s'
                    value_copy = value + timedelta(days=1)
                    params.append(value_copy)
                else:
                    query += f'{key} = %s'
                    params.append(value)

                if current_index < (dict_size - 1):
                    query += ' AND '

                current_index += 1

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            cursor.execute(query, params)
            result = cursor.fetchone()

            count = result["count"]

            conn.close()
            

        except Exception as exception:
            print("count_elements: ", exception)
            return None

        return count