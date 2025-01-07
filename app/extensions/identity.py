from oic.oic import Client
from oic.oic.message import AuthorizationResponse
from oic.oauth2.exception import GrantError
from oic.oic import Grant
from oic import rndstr
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from config import CLIENT_ID, CLIENT_SECRET, AUTHORITY, REDIRECT_URI
from flask import session, redirect, url_for
from jwt import decode, InvalidTokenError
from typing import Union
import functools

class staticproperty(staticmethod):
    def __get__(self, *_):
        return self.__func__()
    
class token(str):
    def __new__(cls, value):
        return str.__new__(cls, value)
    
    def __init__(self, value):
        self.value = value

    def is_valid(self):
        # check if the date is expired
        try:
            _ = decode(self, verify=True)
            return True
        except InvalidTokenError:
            return False

    def parse(self) -> dict:
        # parse the base64 encoded token
        return decode(self, verify=False)
        

class Identity:

    __client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    __client.provider_config(AUTHORITY)
    __client.store_registration_info({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uris": [REDIRECT_URI],
    })
    
    @staticmethod
    def get_authorization_url() -> str:
        session["state"] = rndstr()
        session["nonce"] = rndstr()

        return Identity.__client.construct_AuthorizationRequest(
            request_args={
                "response_type": "code",
                "scope": ["openid", "email", "profile"],
                "redirect_uri": REDIRECT_URI,
                "state": session["state"],  
                "nonce": session["nonce"]
            }
        ).request(Identity.__client.authorization_endpoint)
    
    @staticmethod
    def get_access_token(code) -> str:
        state = session["state"]

        response = AuthorizationResponse(
            code=code,
            state=state
        )

        Identity.__client.grant[state] = Grant()
        Identity.__client.grant[state].add_code(response)

        token_response = Identity.__client.do_access_token_request(
            state=state,
            request_args={
                "code": code
            },
            authn_method="client_secret_basic"
        )

        session["access_token"] = token_response["access_token"]
        session["id_token"] = token_response["id_token"]

        return token(token_response["access_token"])
    
    
    @staticproperty
    def access_token() -> Union[token, None]:
        if session.get("access_token"):
            access_token = token(session["access_token"])
            if access_token.is_valid():
                return access_token
            else:
                session.clear()
                return None
        else:
            return None
        
    @staticmethod
    def logout():
        session.clear()

    @staticmethod
    def get_user_info() -> Union[dict, None]:
        if Identity.access_token:
            try:
                user_info = Identity.__client.do_user_info_request(
                    state=session["state"],
                    authn_method="client_secret_basic",
                    token=Identity.access_token
                )
                user_info.update(session["id_token"])
                return user_info
            except GrantError:
                return None
        else:
            return None
        
    @staticmethod
    def middleguard(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if Identity.access_token:
                return func(*args, **kwargs, user_info=Identity.get_user_info())
            else:
                return redirect(url_for("auth.login"))
        return wrapper