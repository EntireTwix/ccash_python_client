class UserNotExists(Exception):
    def __init__(self, user):
        self.user = user


class InvalidPassword(Exception):
    def __init__(self, user, password):
        self.user = user
        self.password = password

