from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from google.oauth2 import id_token
from google.auth.transport import requests
from typing import Annotated

storage_app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

CLIENT_ID = None

def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    return info



@storage_app.get("/hello")
async def root(token: Annotated[str, Depends(verify_token)]):

    return {"message": f"hello storage, logged as {token['name']}"}
