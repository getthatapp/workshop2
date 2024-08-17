from db_settings import dbSettings
from psycopg2 import connect


def execute_query(query):
    connection = connect(**dbSettings)
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(query)
        try:
            result = cursor.fetchall()
        except:
            result = None
        connection.close()
        return result