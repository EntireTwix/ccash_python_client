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
from exc import UserNotFound, InvalidPassword, InvalidRequest, \
    NameTooLong, UserAlreadyExists, InsufficientFunds \
    ## pylint: disable=import-error
from conf import MAX_NAME_LENGTH    ## pylint: disable=import-error


class CCash:
    def __init__(self, domain: str, timeout=20):
        '''
        `domain`: the domain name or address of a CCash server  
        `timeout`: the timeout duration for a server response
        '''

        self.domain = domain
        self.timeout = timeout


    def help(self):
        '''
        Returns the CCash help page as a byte array
        '''

        return requests.get(
            self.domain + "/BankF/help",
            timeout=self.timeout
        ).content


    def ping(self):
        '''
        Returns a boolean value indicating if the server is online
        '''

        try:
            requests.get(
                self.domain + "/BankF/ping",
                timeout=5
            )
            return True
        except requests.Timeout:
            return False


    def close(self, admin_pw: str):
        '''
        Closes the server and saves its current state  
        Note that this is the only safe way to do so

        `admin_pw`: the administrator password

        Raises (admin) `InvalidPassword`
        '''

        if not requests.post(
            self.domain + "/BankF/admin/close",
            timeout=self.timeout,
            headers=dict(password=admin_pw)
        ).json()["value"]:
            raise InvalidPassword(admin_pw)


    def new_user(self, name: str, init_pw: str):
        '''
        Creates a new user

        `name`: the name of the new user  
        `init_pw`: the initial password of the new user

        Raises `NameTooLong`, `UserAlreadyExists`
        '''

        if len(name) > MAX_NAME_LENGTH:
            raise NameTooLong(name)

        if requests.post(
            self.domain + f"/BankF/user/{name}",
            timeout=self.timeout,
            headers=dict(password=init_pw)
        ).json()["value"] == -5:
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
            data=pw
        ).json()["value"]

        if response == -2:
            raise InvalidPassword(admin_pw)
        elif response == -5:
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
        ).json()["value"]

        if response == -1:
            raise UserNotFound(name)
        elif reponse == -2:
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
        ).json()["value"]

        if response == -1:
            raise UserNotFound(name)
        elif response == -2:
            raise InvalidPassword(admin_pw)
        

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
        ).json()["value"]

        if response == -1:
            raise UserNotExists(name)
        else:
            return bool(response)


    def verify_user(self, name: str):
        '''
        Verifies if a user is on the server

        `name`: the name of the user

        Returns `True` or `False` based on if the user is on the 
        server
        '''

        return bool(requests.get(
            self.domain + "/BankF/contains/" + name,
            timeout=self.timeout
        ).json()["value"])


    def verify_admin_pw(self, admin_pw: str):
        '''
        Verifies the administrator's password of the server 
        instance 

        `admin_pw`: the administrator password of the server 
        instance to verify
        
        Returns `True` or `False` based on whether the password is
        correct
        '''

        return bool(requests.post(
            self.domain + "/BankF/admin/vpass",
            timeout=self.timeout,
            json=dict(attempt=admin_pw)
        ).json()["value"])


    def 
