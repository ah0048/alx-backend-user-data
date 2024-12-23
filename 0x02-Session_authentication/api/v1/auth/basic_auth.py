#!/usr/bin/env python3
'''basic auth class'''
from api.v1.auth.auth import Auth
import binascii
import base64
from typing import Tuple, TypeVar
from models.user import User


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

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        '''
         returns the User instance based on his email and password.
        '''
        if user_email is None or user_pwd is None:
            return None
        elif not isinstance(user_email, str):
            return None
        elif not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        if len(users) == 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        retrieves the User instance for a request
        '''
        auth_header = self.authorization_header(request)
        base64_encoded_value = self.extract_base64_authorization_header(
            auth_header
            )
        base64_decoded_value = self.decode_base64_authorization_header(
            base64_encoded_value
            )
        user_creds = self.extract_user_credentials(base64_decoded_value)
        user = self.user_object_from_credentials(
            user_email=user_creds[0],
            user_pwd=user_creds[1]
            )
        return user
