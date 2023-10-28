class Twit:
    def __init__(self, id, body, author):
        self.id = id
        self.body = body
        self.author = author

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'author_id': self.author.id  # Assuming author is an instance of User
        }