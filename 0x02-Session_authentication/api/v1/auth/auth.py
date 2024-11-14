#!/usr/bin/env python3
'''auth class'''
from flask import request
from typing import List, TypeVar
import os


class Auth:
    '''auth class'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''require auth paths'''
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if path.rstrip('/') == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''header for auth'''
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        '''current user'''
        return None

    def session_cookie(self, request=None):
        ''' returns a cookie value from a request'''
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)
