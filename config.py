import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("OIDC_CLIENT_ID", "client_id")
CLIENT_SECRET = os.getenv("OIDC_CLIENT_SECRET", "client_secret")
AUTHORITY = os.getenv("OIDC_AUTHORITY", "your_authority")
REDIRECT_URI = os.getenv("REDIRECT_URI", "client_redirect_uri")

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    PREFERRED_URL_SCHEME = os.getenv("PREFERRED_URL_SCHEME", "http")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour