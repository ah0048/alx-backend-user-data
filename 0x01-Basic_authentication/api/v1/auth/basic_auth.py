#!/usr/bin/env python3
'''basic auth class'''
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''basic auth class'''

    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        '''
        returns the Base64 part of the Authorization header
        '''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        authorization_header = authorization_header.split()
        if authorization_header[0] != "Basic":
            return None
        else:
            return authorization_header[1]
