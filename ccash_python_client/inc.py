#!/usr/bin/python3
# ccash_python_client - ccash python client
# Copyright (C) 2021 FearlessDoggo21
# see LICENCE file for licensing information

import base64


class User:
    '''Structure to keep track of a username and password pair.'''

    def __init__(self, name: str, passwd: str):
        self.name = name
        self.passwd = passwd


    def __eq__(self, other) -> bool:
        return (self.name, self.passwd) == (other.name, other.passwd)


    def auth_encode(self) -> str:
        # Processing on raw string because `str()` outputs with byte
        # prefix
        return "Basic " + str(base64.standard_b64encode(
            bytes(f"{self.name}:{self.passwd}", "ascii")
        ))[2:-1]

    
    def to_dict(self) -> dict:
        return {"name": self.name, "pass": self.passwd}


def valid_name(self, name: bytes) -> bool:
    '''Verifies if a name is valid on the server.  
    It must be within the name length requirements,
    made of ASCII characters, and lower- alpha-numerical with
    underscores.'''
    if len(name) > 16 or len(name) < 3:
        return False

    # Alpha-numeric check, could be run with python functions
    # yet that is slightly wasteful as it deals with unicode
    for ch in name:
        if not ((ch >= 'a' and ch <= 'z') or
                (ch >= '0' and ch <= '9') or
                (ch == '_')):
            return False

    return True
