#!/usr/bin/env python3
'''
Encrypting passwords
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''function called hash_password that expects one string argument name
    password and returns a salted, hashed password, which is a byte string.'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
