from psycopg2 import connect

dbname = 'parkingcontroldb'
dbuser = 'pablo'
password = 'jd3_Ljks2h'


def get_connection():
    return connect(dbname = dbname, user = dbuser, password =password)