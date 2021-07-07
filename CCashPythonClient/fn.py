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
from .inc import User


class CCash:
    '''The CCash client class'''

    def __init__(self, domain: str, timeout=20):
        if domain[-1] != '/':
            domain += '/'

        properties = requests.get(
            domain + "api/properties"
        ).json()

        self.version  = properties["version"]
        self.name_max = properties["max_name"]
        self.name_min = properties["min_name"]
        self.log_max  = properties["max_log"]

        self.domain = domain + "api/v" + str(self.version)
        self.timeout = timeout


    def valid_name(self, name: bytes) -> bool:
        '''Verifies if a name is valid on the server.  
        It must be within the name length requirements,  
        made of ASCII characters, and alpha-numerical with  
        underscores.'''
        if len(name) > self.name_max or len(name) < self.name_min:
            return False

        ## Alpha-numeric check, could be run with python functions
        ## yet that is slightly wasteful as it deals with unicode
        for ch in name:
            if not ((ch >= 'A' and ch <= 'Z') or
                    (ch >= 'a' and ch <= 'z') or
                    (ch >= '0' and ch <= '9') or
                    (ch == '_')):
                return False

        return True


    def close(self, admin: User) -> bool:
        '''Safely closes the server and saves its current state.  
        Returns bool noting whether the credentials were correct
        and the server was able to close.'''
        return requests.post(
            self.domain + "/admin/shutdown",
            timeout=self.timeout,
            headers={"Authorization": admin.auth_encode()}
        ).status_code


    def new_user(self, user: User) -> int:
        '''Creates a new user without an initial balance.'''
        if not self.valid_name(user.name):
            return 400

        ## Status code will be 409 Conflict if user already exists
        return requests.post(
            self.domain + "/user/register",
            timeout=self.timeout,
            json={"name": user.name, "pass": user.passwd}
        ).status_code


    def admin_new_user(self, admin: User, user: User,
            amount: int) -> int:
        '''Creates a new user with an initial balance.'''
        if not self.valid_name(user.name):
            return 400

        return requests.post(
            self.domain + "/admin/user/register",
            timeout=self.timeout,
            headers={"Authorization": admin.auth_encode()},
            json={"name": user.name, "pass": user.passwd, 
                    "amount": amount}
        ).status_code


    def del_user(self, user: User) -> int:
        '''Deletes a user.'''
        return requests.delete(
            self.domain + "/user/delete",
            timeout=self.timeout,
            headers={"Authorization": user.auth_encode()}
        ).status_code


    def admin_del_user(self, admin: User, name: str) -> int:
        '''Deletes a user via the admin password.'''
        return requests.delete(
            self.domain + "/admin/user/delete",
            timeout=self.timeout,
            headers={"Authorization": admin.auth_encode()},
            json={"name": name}
        ).status_code


    def user_exists(self, name: str) -> bool:
        '''Confirms if a user exists.'''
        return requests.get(
            self.domain + f"/user/exists?name={name}",
            timeout=self.timeout
        ).content == "true"


    def verify_passwd(self, user: User) -> bool:
        '''Confirms a users password.  
        If a `False` value returned, the user may not exist.'''
        return requests.get(
            self.domain + "/user/verify_password",
            timeout=self.timeout,
            headers={"Authorization": user.auth_encode()}
        ).content == "true"


    def verify_admin(self, admin: User) -> bool:
        '''Confirms the admin account.'''
        return requests.post(
            self.domain + "/admin/verify_account",
            timeout=self.timeout,
            headers={"Authorization": admin.auth_encode()}
        ).content == "true"


    def change_passwd(self, user: User, passwd: str) -> int:
        '''Changes a user password.'''
        return requests.patch(
            self.domain + "/user/change_password",
            timeout=self.timeout,
            headers={"Authorization": user.auth_encode()},
            json={"pass": passwd}
        ).status_code


    def admin_change_passwd(self, admin: User, name: str,
            passwd: str) -> int:
        '''Changes a user password via the admin password.'''
        return requests.patch(
            self.domain + "/admin/user/change_password",
            timeout=self.timeout,
            headers={"Authorization": admin.auth_encode()},
            json={"name": name, "pass": passwd}
        ).status_code


    def get_bal(self, name: str):
        '''Gets the balance of a user.  
        Returns 0 if the user does not exist.'''
        response = requests.get(
            self.domain + f"/user/balance?name={name}",
            timeout=self.timeout
        )
        return int(str(response.content)[2:-1]) if response.status_code \
                == 200 else 0


    def set_bal(self, admin: User, name: str, balance: int) -> int:
        '''Sets the balance of a user.'''
        return requests.patch(
            self.domain + "/admin/set_balance",
            timeout=self.timeout,
            headers={"Authorization": admin.auth_encode()},
            json={"name": name, "amount": balance}
        ).status_code


    def impact_bal(self, admin: User, name: str, amount: int) -> int:
        '''Offsets the balance of a user.'''
        return requests.post(
            self.domain + "/admin/impact_balance",
            timeout=self.timeout,
            headers={"Authorization": admin.auth_encode()},
            json={"name": name, "amount": amount}
        ).status_code


    def get_logs(self, user: User) -> dict:
        '''Returns the logged transactions of a user.'''
        return requests.get(
            self.domain + "/user/log",
            timeout = self.timeout,
            headers={"Authorization": user.auth_encode()}
        ).json()


    def send(self, user: User, name: str, amount: str) -> int:
        '''Sends an amount to another user.'''
        return requests.post(
            self.domain + "user/transfer",
            timeout=self.timeout,
            headers={"Authorization": user.auth_encode()},
            json={"name": name, "amount": amount}
        ).status_code
