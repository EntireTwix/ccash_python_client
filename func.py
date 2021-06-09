import requests


class CCash:
    '''
    The configuration class for CCash server communication  
    '''

    def __init__(self, domain: str, timeout=20):
        '''
        Initializes a new instance of the CCash class

        `domain`: the domain name of the server hosting CCash  
        `timeout`: the maximum amount of time to wait for a server
        response
        '''

        self.domain = domain
        self.timeout = timeout


    def close(self, admin_pw: str):
        '''
        Closes and saves the server instance

        `admin_pw`: the administrator password of the server instance
        '''

        requests.post(
            self.domain + "/BankF/admin/close",
            timeout=self.timeout,
            json=dict(attempt=admin_pw)
        )


    def new_user(self, name: str, pw: str):
        '''
        Creates a new user

        `name`: the name of the new user  
        `pw`: the initial password of the new user
        '''

        requests.post(
            self.domain + "/BankF/user",
            timeout=self.timeout,
            json=dict(name=name, init_pass=pw)
        )


    def admin_new_user(self, name: str, pw: str, bal: int, 
        admin_pw: str):
        '''
        Creates a new user with an initial balance greater than 0

        `name`: the name of the new user  
        `pw`: the initial password of the new user  
        `bal`: the initial balance of the new user  
        `admin_pw`: the administrator password of the server instance
        '''

        requests.post(
            self.domain + "/BankF/admin/user",
            timeout=self.timeout,
            json=dict(name=name, init_pass=pw, init_bal=bal, 
                attempt=admin_pw)
        )

