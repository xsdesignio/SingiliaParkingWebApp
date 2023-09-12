from psycopg2 import connect
import os


dbname = os.environ.get('DB_NAME')
dbuser = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')


def get_connection():
    return connect(dbname = dbname, user = dbuser, password =password)