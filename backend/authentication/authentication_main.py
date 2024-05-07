
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
# https://developers.google.com/identity/protocols/oauth2/web-server
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'authentication/client_secret.json',
    scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile'])
flow.redirect_uri = 'http://localhost:8000/auth/callback'

CLIENT_ID = None


def verify_token(token):
    info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    return info


@auth_app.get("/hello")
async def root():
    return {"hello" : ["kruk", "tomek", "tomasz"]}


@auth_app.get("/login")
async def login():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='select_account'
    )
    return RedirectResponse(url=authorization_url)


@auth_app.get("/callback")
async def callback(request: Request):
    try:
        token_dict = flow.fetch_token(authorization_response=str(request.url))
        # token_dict['id_token'] += "AA"         # modyfikacja tokenu powoduje błąd i następuje przekierowanie do ponownego logowania
        verify_token(token_dict["id_token"])
        return token_dict["id_token"]

    except Exception:
        return RedirectResponse(url="http://localhost:8000/auth/login")
