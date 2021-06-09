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

class UserNotExists(Exception):
    '''
    Exception for a user that does not exist within the server
    '''

    def __init__(self, name: str):
        '''
        `name`: the name of a user not within the server
        '''

        self.name = name


class InvalidPassword(Exception):
    '''
    Exception for an incorrect password
    '''

    def __init__(self, name: str, pw: str):
        '''
        `name`: the name of the user  
        `pw`: the invalid password
        '''

        self.name = name
        self.pw = pw


class InadequatePermissions(Exception):
    '''
    Exception for an incorrect administrator password
    '''

    def __init__(self, admin_pw: str):
        '''
        `admin_pw`: the invalid administrator password
        '''

        self.admin_pw = admin_pw


class NameTooLong(Exception):
    '''
    Excepttion for a name that is too long
    '''

    def __init__(self, name: str):
        '''
        `name`: the name that is too long
        '''

        self.name = name
