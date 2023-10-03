from datetime import timedelta
from .db_connection import get_connection
from psycopg2 import extras
from typing import Optional



class BaseModel:


    @classmethod
    def delete_element(cls, table, id):
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(f'DELETE FROM { table } WHERE id= %s', (id,))
            conn.commit()
            conn.close()
        except Exception as exception:
            print("delete_element: ", exception)
            return False
        
        return True


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
    def get_elements_from_start(cls, table: str, interval: Optional[tuple[int, int]] = None, **kwargs) -> list[dict]:
        """Get a list with the elements of the table that match the provided parameters (kwargs). It starts from the first element in the table is ascending order. (so the first element shown if exists is the oldest one added, the one with id = 0)
        
        Keyword arguments:
        table -- the name of the table to query
        interval -- an optional tuple with the start and end index of the elements to return
        kwargs -- the parameters to filter the query
        Return: the list with the elements
        """


        if interval is None:
            interval = (0, 50)
        
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
        if interval:
            limit = interval[1] - interval[0]
            offset = interval[0]
            query += f' LIMIT %s OFFSET %s'
            params.extend([limit, offset])

        # Execute the query
        try:
            with get_connection() as conn:
                cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
                cursor.execute(query, tuple(params))
                result = cursor.fetchall()

        except Exception as exception:
            print("get_elements: ", exception)
            return None
        
        return result



    @classmethod
    def get_elements(cls, table: str, interval: Optional[tuple[int, int]] = None, **kwargs) -> list[dict]:
        """Get a list with the elements of the table that match the provided parameters (kwargs) in descending order (so the first elements is the newest one added)
        
        Keyword arguments:
        table -- the name of the table to query
        interval -- an optional tuple with the start and end index of the elements to return
        kwargs -- the parameters to filter the query
        Return: the list with the elements
        """


        if interval is None:
            interval = (0, 50)

        
        query = f'SELECT * FROM { table }'
        params = []

        # Build the SQL query dynamically based on the provided parameters
        if kwargs:
            query += ' WHERE '

            for index, (key, value) in enumerate(kwargs.items()):
                if key == 'start_date':
                    query += f'created_at > %s'
                    value -= timedelta(days=1)
                elif key == 'end_date':
                    query += f'created_at < %s'
                    value += timedelta(days=1)
                else:
                    query += f'{key} = %s'

                params.append(value)

                if index < len(kwargs) - 1:
                    query += ' AND '


        query += ' ORDER BY created_at DESC'

        # Add LIMIT and OFFSET if a range is provided
        if interval :
            limit = interval[1] - interval[0]
            offset = interval[0]
            query += f' LIMIT %s OFFSET %s'
            params.extend([limit, offset])

        # Execute the query
        try:
            with get_connection() as conn:
                cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
                print(query, tuple(params))
                cursor.execute(query, tuple(params))
                result = cursor.fetchall()

        except Exception as exception:
            print("get_elements: ", exception)
            return []
        
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
    
