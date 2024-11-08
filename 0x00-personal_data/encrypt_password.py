#!/usr/bin/env python3
'''
Encrypting passwords
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''function called hash_password that expects one string argument name
    password and returns a salted, hashed password, which is a byte string.'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''function called is_valid that expects 2 arguments: hashed_password,
    which is a bytes type, and password, which is a string type. This function
    returns a boolean.'''
    return bcrypt.checkpw(password.encode(), hashed_password)
