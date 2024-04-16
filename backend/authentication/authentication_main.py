import json

from fastapi import FastAPI

import google_auth_oauthlib.flow
from fastapi import Request
from starlette.responses import RedirectResponse
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
auth_app = FastAPI(debug=True)

# https://developers.google.com/identity/protocols/oauth2/web-server
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'authentication/client_secret.json',
    scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile'])
flow.redirect_uri = 'http://localhost:8000/auth/callback'


@auth_app.get("/hello")
async def root():
    return {"message": "hello auth"}


@auth_app.get("/login")
async def login():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='select_account'
    )
    return RedirectResponse(url=authorization_url)


@auth_app.get("/callback")
async def callback(request: Request):
    flow.fetch_token(authorization_response=str(request.url))
    return json.loads(flow.credentials.to_json())
