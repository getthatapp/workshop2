from common.crypto import hash_password
from queries.sql_queries import Query


class User:

    def __init__(self, username=None, password=None, salt=None):
        self._id = None
        self.username = username
        if password is not None:
            self._hashed_password = hash_password(password, salt)
        else:
            self._hashed_password = None

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=None):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self):
        if self._id is None:
            self._id = Query.save_user_to_database(self.username, self._hashed_password)
        else:
            Query.update_user_in_db(self.username, self._hashed_password, self._id)

    @staticmethod
    def load_user_by_id(id_):
        data = Query.get_user_by_id(id_)
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        return None

    @staticmethod
    def load_user_by_username(username):
        data = Query.get_user_by_username(username)
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        return None

    @staticmethod
    def load_all_users():
        users = []
        rows = Query.get_all_users()
        for row in rows:
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete_user(self):
        if self._id is not None:
            Query.delete_user_by_id(self._id)
            self._id = None
            return True
        return False


