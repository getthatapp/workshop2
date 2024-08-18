from queries.sql_queries import Query


class Message:

    def __init__(self, from_id, to_id, text):
        self._id = None
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_date = None

    @property
    def creation_date(self):
        return self._creation_date

    @property
    def id(self):
        return self._id

    @staticmethod
    def load_all_messages(user_id=None):
        rows = Query.get_all_messages(user_id)
        messages = []
        for row in rows:
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Message(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message._creation_date = creation_date
            messages.append(loaded_message)
        return messages

    def save_to_db(self):
        if self._id is None:
            result = Query.save_message(self.from_id, self.to_id, self.text)
            if result:
                self._id, self._creation_date = result
            return True
        else:
            Query.update_message(self._id, self.from_id, self.to_id, self.text)
            return True

