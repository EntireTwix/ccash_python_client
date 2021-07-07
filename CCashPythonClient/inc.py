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

import base64


class User:
    '''Structure to keep track of a username and password pair.'''

    def __init__(self, name: str, passwd: str):
        self.name = name
        self.passwd = passwd


    def __eq__(self, other) -> bool:
        return (self.name, self.passwd) == (other.name, other.passwd)


    def auth_encode(self) -> str:
        ## Processing on raw string because `str()` outputs with byte
        ## prefix
        return "Basic " + str(base64.standard_b64encode(
            bytes(f"{self.name}:{self.passwd}", "ascii")
        ))[2:-1]
