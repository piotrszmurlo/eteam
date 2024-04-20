from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    return info
