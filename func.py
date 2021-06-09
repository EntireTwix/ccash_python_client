import requests
from exc import UserNotExists, InvalidPassword  ## pylint: disable=import-error


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


    def send_funds(self, sender: str, pw: str, receiver: str, 
        amount: int):
        '''
        Sends money from one user to another

        `sender`: the name of the sender  
        `pw`: the password of the sender  
        `receiver`: the name of the receiver  
        `amount`: the amount to send
        '''

        requests.post(
            self.domain + "/BankF/sendfunds",
            timeout=self.timeout,
            json=dict(a_name=sender, attempt=pw, b_name=receiver,
                amount=amount)
        )


    def change_pw(self, name: str, pw: str, new_pw: str):
        '''
        Changes a user's password

        `name`: the name of the user  
        `pw`: the user's original password which they want to 
        change  
        `new_pw`: the new password

        Raises a `UserNotExists` error if the user is not on the 
        server
        '''

        if requests.patch(
            self.domain + "/BankF/changepass",
            timeout=self.timeout,
            json=dict(name=name, attempt=pw, new_pass=new_pw)
        ).json().get("value") == -1:
            raise UserNotExists(name)


    def admin_set_bal(self, name: str, admin_pw: str, bal: int):
        '''
        Sets a user's balance

        `name`: the name of the user  
        `admin_pw`: the administrator password of the server 
        instance  
        `bal`: the new balance of the user
        '''

        requests.patch(
            self.domain + "/BankF/" + name + "/bal",
            timeout=self.timeout,
            json=dict(name=name, attempt=admin_pw, amount=bal)
        )


    def help(self):
        '''
        Gets the CCash help page

        Returns the UTF-8 formatted help texts
        '''

        return requests.get(
            self.domain + "/BankF/help",
            timeout=self.timeout
        ).text


    def verify_pw(self, name: str, pw: str):
        '''
        Verifies a user's password

        `name`: the name of the user  
        `pw`: the password to verify

        Returns `True` or `False` based on whether the password is
        correct

        Raises a `UserNotExists` error if the user is not on the 
        server
        '''

        response = requests.post(
            self.domain + "/BankF/vpass",
            timeout=self.timeout,
            json=dict(name=name, attempt=pw)
        ).json().get("value")

        if response == -1:
            raise UserNotExists(name)
        else:
            return bool(response)