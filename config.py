import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("OIDC_CLIENT_ID", "client_id")
CLIENT_SECRET = os.getenv("OIDC_CLIENT_SECRET", "client_secret")
AUTHORITY = os.getenv("OIDC_AUTHORITY", "your_authority")
REDIRECT_URI = os.getenv("REDIRECT_URI", "client_redirect_uri")

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    PREFERRED_URL_SCHEME = os.getenv("PREFERRED_URL_SCHEME", "https")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")