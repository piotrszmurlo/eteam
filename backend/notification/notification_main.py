from typing import Annotated

from fastapi import FastAPI, Depends

from common.dependencies import verify_token
from notification.models import UserIdResponse, UserModel, UserEmailInput
from notification.repository import NotificationRepository


notification_app = FastAPI()


@notification_app.get("/hello")
async def root():
    return {"message": "hello notification"}


@notification_app.post("/user")
async def add_user(user_email: UserEmailInput, token: Annotated[str, Depends(verify_token)]) -> UserIdResponse:
    notification_repo = NotificationRepository()
    user = UserModel(user_id=token["sub"], user_name=token["given_name"], user_email=user_email.user_email)
    user_id = notification_repo.insert_user(user)
    return UserIdResponse(user_id=user_id)