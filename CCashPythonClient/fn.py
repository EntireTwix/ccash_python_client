## Copyright © 2021 FearlessDoggo21
## 
## Permission is hereby granted, free of charge, to any person
## obtaining a copy of this software and associated documentation
## files (the “Software”), to deal in the Software without
## restriction, including without limitation the rights to use, copy,
## modify, merge, publish, distribute, sublicense, and/or sell copies
## of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
## 
## The above copyright notice and this permission notice shall be
## included in all copies or substantial portions of the Software.
## 
## THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
## EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
## MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
## NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
## HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
## WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
## DEALINGS IN THE SOFTWARE.

import requests
from .ex import BadRequest, Unauthorized, NotFound
from .inc import User


class CCash:
    '''
    The CCash client class
    '''

    def __init__(self, domain: str, timeout=20):
        properties = requests.get(
            domain + "/api/properties"
        ).json()

        self.version  = properties["version"]
        self.name_max = properties["max_name"]
        self.name_min = properties["min_name"]
        self.log_max  = properties["max_log"]

        self.domain = domain + "/api/v" + str(self.version)
        self.timeout = timeout


    def valid_name(self, name: bytes) -> bool:
        '''
        Returns a boolean value indicating whether the input is a
        valid name.
        '''

        if len(name) > self.name_max or len(name) < self.name_min:
            return False
        
        ## Alpha-numeric check, could be run with python functions
        ## yet that is slightly wasteful as it deals with unicode
        for ch in name:
            if not ((ch >= 'A' and ch <= 'Z') or
                    (ch >= 'a' and ch <= 'z') or
                    (ch >= '0' and ch <= '9') or
                    ch == '_'):
                return False

        return True


    def close(self, admin: User) -> bool:
        '''
        Safely closes the server and saves its current state.  
        Returns a boolean value based on whether the credentials were
        correct.
        '''
        
        return requests.post(
            self.domain + "/admin/shutdown",
            timeout=self.timeout,
            headers={"Authorization": admin.auth_encode()}
        ).content == "true"


    def new_user(self, name: str, init_pw: str):
        '''
        Creates a new user without an initial balance
        '''
        if requests.post(
            self.domain + f"/BankF/user/{name}",
            timeout=self.timeout,
            headers=dict(password=init_pw)
        ).json == "-5":
            raise UserAlreadyExists(name)


    def admin_new_user(self, name: str, init_pw: str, bal: int, 
        admin_pw: str):
        '''
        Creates a new user with an initial balance greater than 0

        `name`: the name of the new user  
        `init_pw`: the initial password of the new user  
        `bal`: the initial balance of the new user  
        `admin_pw`: the administrator password

        Raises (admin) `InvalidPassword`, `NameTooLong`
        '''

        if len(name) > MAX_NAME_LENGTH:
            raise NameTooLong(name)

        response = requests.post(
            self.domain + f"/BankF/admin/user/{name}?init_bal={bal}",
            timeout=self.timeout,
            headers=dict(password=admin_pw),
            data=init_pw
        ).content

        if response == "-2":
            raise InvalidPassword(admin_pw)
        elif response == "-5":
            raise UserAlreadyExists(name)


    def del_user(self, name: str, pw: str):
        '''
        Deletes a user

        `name`: the name  
        `pw`: the password

        Raises `UserNotFound`, `InvalidPassword`
        '''

        response = requests.delete(
            self.domain + f"/BankF/user/{name}",
            timeout=self.timeout,
            headers=dict(password=pw)
        ).content

        if response == "-1":
            raise UserNotFound(name)
        elif response == "-2":
            raise InvalidPassword(pw, name)


    def admin_del_user(self, name: str, admin_pw: str):
        '''
        Deletes a user with the administrator password

        `name`: the name  
        `admin_pw`: the administrator password

        Raises `UserNotFound`, (admin) `InvalidPassword`
        '''

        response = requests.delete(
            self.domain + f"/BankF/admin/user/{name}",
            timeout=self.timeout,
            headers=dict(password=admin_pw)
        ).content

        if response == "-1":
            raise UserNotFound(name)
        elif response == "-2":
            raise InvalidPassword(admin_pw)


    def user_exists(self, name: str):
        '''
        Returns a boolean value indicating if a user exists

        `name`: the name
        '''

        return requests.get(
            self.domain + f"/BankF/contains/{name}",
            timeout=self.timeout
        ).content != "-2"


    def verify_pw(self, name: str, pw: str):
        '''
        Returns a boolean value indicating if the supplied password
        is that of the user

        `name`: the name  
        `pw`: the password

        Raises `UserNotFound`
        '''

        response = requests.get(
            self.domain + f"/BankF/{name}/pass/verify",
            timeout=self.timeout,
            headers=dict(password=pw)
        ).content

        if response == "-1":
            raise UserNotFound(name)
        
        return response != "-2"


    def verify_admin_pw(self, admin_pw: str):
        '''
        Returns a boolean value indicating if the supplied password
        is the administrator password

        `admin_pw`: the administrator password
        '''

        return requests.get(
            self.domain + "/BankF/admin/verify",
            timeout=self.timeout,
            headers=dict(password=admin_pw)
        ).content == "-2"

    
    def change_pw(self, name: str, pw: str, change_pw: str):
        '''
        Changes a user's password

        `name`: the name  
        `pw`: the password  
        `change_pw`: the password to change to

        Raises `UserNotFound`, `WrongPassword`
        '''

        response = requests.patch(
            self.domain + f"/BankF/{name}/pass/change",
            timeout=self.timeout,
            headers=dict(password=pw),
            body=change_pw
        ).content

        if response == "-1":
            raise UserNotFound(name)
        elif response == "-2":
            raise InvalidPassword(pw, name)


    def get_bal(self, name: str):
        '''
        Returns a user's balance

        `name`: the name

        Raises `UserNotFound`
        '''

        response = int(requests.get(
            self.domain + f"/BankF/{name}/bal",
            timeout=self.timeout
        ).content)

        if response == -1:
            raise UserNotFound(name)
        
        return response


    def set_bal(self, name: str, admin_pw: str, amount: int):
        '''
        Sets a user's balance

        `name`: the name  
        `admin_pw`: the administrator password  
        `amount`: the amount to set

        Raises `UserNoutFound`, (admin) `InvalidPassword`
        '''

        response = requests.patch(
            self.domain + f"/BankF/admin/{name}/bal?amount={amount}",
            timeout=self.timeout,
            headers=dict(password=admin_pw)
        ).content

        if response == "-1":
            raise UserNotFound(name)
        elif response == "-2":
            raise InvalidPassword(admin_pw)


    def get_log(self, name: str, pw: str):
        '''
        Returns a user's logs

        `name`: the name
        `pw`: the password

        Raises `UserNotFound`, `InvalidPassword`
        '''

        response = requests.get(
            self.domain + f"/BankF/{name}/log",
            timeout = self.timeout,
            headers=dict(password=pw)
        ).json()

        if response == -1:
            raise UserNotFound(name)
        elif response == -2:
            raise InvalidPassword(pw, name)

        return response

    
    def send_funds(self, sender: str, pw: str, recipient: str, 
        amount: int):
        '''
        Sends an amount to another user

        `sender`: the name of the sender  
        `pw`: the password of the sender  
        `recipient`: the name of the recipient  
        `amount`: the amount to send

        Raises `UserNotFound`, `InvalidPassword`, `InvalidRequest`,
        `InsufficientFunds`
        '''

        response = requests.post(
            self.domain + 
                f"/BankF/{sender}/send/{recipient}?amount={amount}",
            timeout=self.timeout,
            headers=dict(password=pw)
        ).content

        if response == "-1":
            raise UserNotFound(None)
        elif response == "-2":
            raise InvalidPassword(pw, sender)
        elif response == "-3":
            raise InvalidRequest()
        elif response == "-6":
            raise InsufficientFunds(sender, amount)
