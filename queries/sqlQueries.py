from common.dbSettings import dbSettings
from psycopg2 import connect


class Query:

    def executeQuery(query):
        conn = connect(**dbSettings)
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query)
            try:
                result = cursor.fetchall()
            except:
                result = None
            conn.close()
            return result

    def updateSQL(query):
        conn = connect(**dbSettings)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    def saveUserToDatabase(username, hashedPassword):
        saveUser = "INSERT INTO users(username, hashedPassword) VALUES(%s, %s) RETURNING id"
        result = Query.executeQuery(saveUser, (username, hashedPassword))
        return result

    def updateUser(username, hashedPassword, id):
        updateUser = "UPDATE users SET username=%s, hashedPassword=%s WHERE id=%s"
        result = Query.executeUpdate(updateUser, (username, hashedPassword, id))
        return result

