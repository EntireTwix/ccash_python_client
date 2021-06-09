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
from exc import UserNotExists, InvalidPassword, \
    InadequatePermissions, NameTooLong \
    ## pylint: disable=import-error


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


    def help(self):
        '''
        Gets the CCash help page

        Returns the UTF-8 formatted help texts
        '''

        return requests.get(
            self.domain + "/BankF/help",
            timeout=self.timeout
        ).text


    def close(self, admin_pw: str):
        '''
        Closes and saves the server instance

        `admin_pw`: the administrator password of the server instance
        '''

        if requests.post(
            self.domain + "/BankF/admin/close",
            timeout=self.timeout,
            json=dict(attempt=admin_pw)
        ).json()["value"] == -1:
            raise InadequatePermissions(admin_pw)


    def new_user(self, name: str, pw: str):
        '''
        Creates a new user

        `name`: the name of the new user  
        `pw`: the initial password of the new user

        Raises a `NameTooLong` error if the name is too long
        '''

        if len(name) > 50:
            raise NameTooLong(name)

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
