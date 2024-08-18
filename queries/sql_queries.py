from common.db_settings import db_settings
from psycopg2 import connect


class Query:

    @staticmethod
    def execute_query(query, params=None, fetchOne=False):
        conn = connect(**db_settings)
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            try:
                if fetchOne:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()
            except:
                result = None
            conn.close()
            return result

    def execute_update(query, params=None):
        conn = connect(**db_settings)
        with conn.cursor() as cursor:
            cursor.execute(query, params)
        conn.commit()
        conn.close()

    @staticmethod
    def save_user_to_database(username, hashed_password):
        saveUser = "INSERT INTO users(username, hashed_password) VALUES(%s, %s) RETURNING id"
        result = Query.execute_query(saveUser, (username, hashed_password), fetchOne=True)
        return result

    @staticmethod
    def update_user_in_db(username, hashed_password, id):
        update_user = "UPDATE users SET username=%s, hashed_password=%s WHERE id=%s"
        Query.execute_update(update_user, (username, hashed_password, id))

    @staticmethod
    def get_user_by_id(id):
        get_user_id = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        result = Query.execute_query(get_user_id, (id, ), fetchOne=True)
        return result

    @staticmethod
    def get_user_by_username(username):
        get_user_name = "SELECT id, username, hashed_password FROM users WHERE username=%s"
        result = Query.execute_query(get_user_name, (username, ), fetchOne=True)
        return result

    @staticmethod
    def get_all_users():
        get_users = "SELECT id, username, hashed_password FROM users"
        result = Query.execute_query(get_users)
        return result

    @staticmethod
    def delete_user_by_id(id):
        delete_user = "DELETE FROM users WHERE id=%s"
        Query.execute_query(delete_user, (id, ))

    @staticmethod
    def save_message(from_id, to_id, text):
        save_message = "INSERT INTO messages(from_id, to_id, text) VALUES(%s, %s, %s) RETURNING id, creation_date"
        result = Query.execute_query(save_message, (from_id, to_id, text), fetchOne=True)
        return result

    @staticmethod
    def update_message(message_id, from_id, to_id, text):
        update_message = "UPDATE messages SET from_id=%s, to_id=%s, text=%s WHERE id=%s"
        Query.executeUpdate(update_message, (from_id, to_id, text, message_id))

    @staticmethod
    def get_all_messages(id=None):
        if id:
            get_all_messages = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id=%s"
            result = Query.execute_query(get_all_messages, (id, ))
        else:
            get_all_messages = "SELECT id, from_id, to_id, text, creation_date FROM messages"
            result = Query.execute_query(get_all_messages)
        return result

