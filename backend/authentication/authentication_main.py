
from fastapi import FastAPI

import google_auth_oauthlib.flow
import google_auth_oauthlib.interactive
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import os

origins = [
    "http://localhost:3000",
]

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
auth_app = FastAPI(debug=True)
auth_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'authentication/client_secret.json',
    scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile'])

CLIENT_ID = flow.client_config["client_id"]


def verify_token(token):
    info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    return info


@auth_app.post("/token")
async def token(token: dict):
    info = verify_token(token['token'])
    return info