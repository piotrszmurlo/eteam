from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from common.dependencies import verify_token
from notification.models import UserIdResponse, UserModel, UserEmailInput
from notification.repository import NotificationRepository
from notification.exceptions import UserAlreadyExists, UserDoesNotExist


notification_app = FastAPI()


@notification_app.get("/hello")
async def root():
    return {"message": "hello notification"}


@notification_app.post("/user")
async def add_user(user_email: UserEmailInput, token: Annotated[str, Depends(verify_token)]) -> UserIdResponse:
    notification_repo = NotificationRepository()
    user = UserModel(user_id=token["sub"], user_name=token["given_name"], user_email=user_email.user_email)
    try:
        user_id = notification_repo.insert_user(user)
    except UserAlreadyExists:
        existing_user_name = token["given_name"]
        raise HTTPException(status_code=400, detail=f"User {existing_user_name} already exists!")
    return UserIdResponse(user_id=user_id)

@notification_app.get("/user")
async def get_user_email(token: Annotated[str, Depends(verify_token)]) -> UserModel:
    notification_repo = NotificationRepository()
    user_id=token["sub"]
    try:
        email = notification_repo.get_user(user_id=user_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail=f"User does not exist!")
    return email