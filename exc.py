class UserNotExists(Exception):
    '''
    Exception for a user that does not exist within the server
    '''

    def __init__(self, user: str):
        '''
        Initializes a new instance of the UserNotExists exception

        `user`: the username of a user not within the server
        '''

        self.user = user


class InvalidPassword(Exception):
    '''
    Exception for an incorrect password
    '''

    def __init__(self, user: str, pw: str):
        '''
        Initializes a new instance of the InvalidePassword exception

        `user`: the username of the user  
        `pw`: the invalid password
        '''

        self.user = user
        self.pw = pw

