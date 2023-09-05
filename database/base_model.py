from datetime import timedelta
from .db_connection import get_connection
from psycopg2 import extras
from typing import Optional



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
    def get_elements(cls, table: str, range: Optional[tuple] = [0, 50], **kwargs) -> list[dict]:
        """Get a list with the elements of the table that match the provided parameters (kwargs)
        
        Keyword arguments:
        table -- the name of the table to query
        range -- an optional tuple with the start and end index of the elements to return
        Return: the list with the elements
        """
        
        query = f'SELECT * FROM { table }'
        params = []

        # Build the SQL query dynamically based on the provided parameters
        if kwargs:
            query += ' WHERE '

            for index, (key, value) in enumerate(kwargs.items()):
                if key == 'start_date':
                    query += f'created_at >= %s'
                    value -= timedelta(days=1)
                elif key == 'end_date':
                    query += f'created_at <= %s'
                    value += timedelta(days=1)
                else:
                    query += f'{key} = %s'

                params.append(value)

                if index < len(kwargs) - 1:
                    query += ' AND '

        # Add LIMIT and OFFSET if a range is provided
        if range:
            limit = range[1] - range[0]
            offset = range[0]
            query += f' LIMIT %s OFFSET %s'
            params.extend([limit, offset])

        # Execute the query
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            cursor.execute(query, tuple(params))
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