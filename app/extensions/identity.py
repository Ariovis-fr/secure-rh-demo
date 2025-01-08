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
    def get_access_token(code, state=None) -> str:
        if state is None:
            return redirect(url_for("auth.login"))

        auth_response = AuthorizationResponse(
            code=code,
            state=state
        )

        grant = Grant()
        grant.add_code(auth_response)
        Identity.__client.grant[state] = grant

        token_response = Identity.__client.do_access_token_request(
            state=state,
            request_args={
                "code": code,
                "redirect_uri": REDIRECT_URI
            },
            authn_method="client_secret_basic"
        )
        
        if token_response.get("error"):
            raise RuntimeError(token_response["error_description"])

        session["access_token"] = token_response["access_token"]

        return token_response["access_token"]
    
    
    @staticproperty
    def access_token() :
        if session.get("access_token"):
            return session["access_token"]
        else:
            session.clear()
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
                return user_info
            except GrantError:
                raise InvalidTokenError("Invalid token")
        else:
            raise InvalidTokenError("No token available")
        
    @staticmethod
    def middleguard(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs, user_info=Identity.get_user_info())
            except InvalidTokenError:
                return redirect(url_for("auth.login"))
        return wrapper