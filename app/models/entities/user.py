from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, email, password, name) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.name = name

    
