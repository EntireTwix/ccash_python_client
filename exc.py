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

class UserNotFound(Exception):
    '''Raised if a user does not exist'''
    def __init__(self, name: str):
        '''
        `name`: the name of the user that does not exist
        '''

        self.name = name


class InvalidPassword(Exception):
    '''Raised if a user or admin password is incorrect'''
    def __init__(self, pw: str, name=None):
        '''
        `pw`: the invalid password  
        `name`: the name of the user, `None` if admin password
        incorrect
        '''

        self.pw = pw
        self.name = name


class InvalidRequest(Exception):
    '''Raised when trying to send funds to self or if amount is 0'''
    pass


class NameTooLong(Exception):
    '''Raised if a name is longer than 50 characters'''
    def __init__(self, name: str):
        '''
        `name`: the name that is too long
        '''

        self.name = name


class UserAlreadyExists(Exception):
    '''Raised when trying to create a user but they already exist'''
    def __init__(self, name: str):
        '''
        `name`: the name of the user that already exists
        '''

        self.name = name


class InsufficientFunds(Exception):
    '''Raised when trying to transfer funds not available'''
    def __init__(self, name: str, amount: int):
        '''
        `name`: the name of the user who has insufficient funds
        `amount`: an insufficient amount
        '''

        self.name = name
        self.amount = amount
