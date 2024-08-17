from common.crypto import hashPassword
from queries.sqlQueries import Query


class User:

    def __init__(self, userId=None, username=None, password=None, salt=None):
        self.userId = userId
        self.username = username
        self.hashedPassword = hashPassword(password, salt)

    @property
    def id(self):
        return self.userId

    @property
    def hashedPassword(self):
        return self.hashedPassword

    def setPassword(self, password, salt=None):
        self.hashedPassword = hashPassword(password, salt)

    @hashedPassword.setter
    def hashedPassword(self, password):
        self.setPassword(password)

    def saveToDb(self, username, hashedPassword):
        if self.id is None:
            Query.saveUserToDatabase(username, hashedPassword)
        else:
            Query.updateUser(username, hashedPassword, self.id)


