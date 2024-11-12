#!/usr/bin/env python3
'''basic auth class'''
from api.v1.auth.auth import Auth
import binascii
import base64
from typing import Tuple


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        '''
        returns the decoded value of a Base64 string
        '''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_string = base64.b64decode(
                base64_authorization_header.encode(),
                validate=True
                )
            return decoded_string.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        '''returns the user email and password from decoded value.'''
        if decoded_base64_authorization_header is None:
            return (None, None)
        elif not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        elif ":" not in decoded_base64_authorization_header:
            return (None, None)
        return (
            decoded_base64_authorization_header.split(":")[0],
            decoded_base64_authorization_header.split(":")[1]
        )
