from oic.oic import Client
from oic.oic.message import AuthorizationResponse
from oic.oauth2.exception import GrantError
from oic.oic import Grant
from oic import rndstr
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic.exception import RequestError
from config import CLIENT_ID, CLIENT_SECRET, AUTHORITY, REDIRECT_URI
from flask import session, redirect, url_for, flash
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
                "scope": ["openid", "email", "profile", "organization"],
                "redirect_uri": REDIRECT_URI,
                "state": session["state"],  
                "nonce": session["nonce"]
            }
        ).request(Identity.__client.authorization_endpoint)
    
    @staticmethod
    def get_access_token(code, state) -> str:

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

        return token_response["access_token"]
    
    
    @staticproperty
    def access_token() :
        if session.get("access_token") and session.get("state"):
            return session["access_token"]
        else:
            return None
        
    @staticmethod
    def logout():
        if not Identity.access_token:
            return None
        try:
            end_session_endpoint = Identity.__client.construct_EndSessionRequest(
                request_args={
                    "state": session["state"]
                }
            )
        except GrantError:
            return None
        url = end_session_endpoint.request(Identity.__client.end_session_endpoint)
        session.clear()
        return url

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
                return None
            except RequestError:
                return None
        else:
            return None
        
    @staticmethod
    def middleguard(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user_info = Identity.get_user_info()
            if user_info:
                return func(*args, **kwargs, user_info=Identity.get_user_info())
            else:
                flash("Unauthorized", "error")
                return redirect(url_for("auth.login"))
        return wrapper