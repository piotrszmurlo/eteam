import json
from fastapi import FastAPI, HTTPException
import google_auth_oauthlib.flow
import google_auth_oauthlib.interactive
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as req
from fastapi import Request
import os
from google.auth import jwt
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
auth_app = FastAPI(debug=True)

# https://developers.google.com/identity/protocols/oauth2/web-server
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'authentication/client_secret.json',
    scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile'])
flow.redirect_uri = 'http://localhost:8000/auth/callback'

CLIENT_ID = None

def verify_token(token):
    info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    return info





@auth_app.get("/callback")
def callback(request: Request):
    token_dict = flow.fetch_token(authorization_response=str(request.url))
    info = verify_token(token_dict["id_token"])
    user_name = info["name"]
    user_sub = info["sub"]

    print(user_name)

    user_data = {
        "name": user_name,
        "sub": user_sub
    }

    add_user_url = "http://localhost:8000/storage/add_user"

    response = req.post(add_user_url, json=user_data)

    return {"message": "User added .."}



@auth_app.get("/hello")
def root():

    user_data = {
        "user_id": 1,
        "name": "Adam",
        "surname": "Mont",
        "company": "Birds"
    }

    add_user_url = "http://localhost:8000/storage/hello"

    response = req.get(add_user_url, json=user_data)

    print(response.json)

    return {"message": "hello auth"}


@auth_app.get("/login")
async def login():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='select_account'
    )
    return RedirectResponse(url=authorization_url)

