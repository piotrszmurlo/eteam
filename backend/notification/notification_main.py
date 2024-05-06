from typing import Annotated

import requests
from fastapi import FastAPI, Depends, HTTPException
from common.dependencies import verify_token
from notification.models import UserIdResponse, UserModel, UserEmailInput, UpgradePlan
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
        raise HTTPException(status_code=400, detail="User does not exist!")
    return email




@notification_app.post("/upgrade_plan")
async def upgrade_plan(upgrade_details: UpgradePlan, token: Annotated[str, Depends(verify_token)]):
# async def upgrade_plan(upgrade_details: UpgradePlan):

    print(f"NOTIFICATION: Your current plan is {upgrade_details.current_plan_name} and you need to upgrade to {upgrade_details.upgrade_plan_name}")


    # TODO:
    # - poprosić create_payment o link podając nowy plan
    # - printujemy link

    # - 


    # payment_url = requests.post('http://localhost:8000/payment/create_payment')

    # print(f"Here is link: {payment_url}")

    return upgrade_details.upgrade_plan_name



@notification_app.get("/upgrade_plan_success")
async def upgrade_plan_success(token: Annotated[str, Depends(verify_token)]):
    return {"message": "Your plan has been upgraded."}

@notification_app.get("/upgrade_plan_fail")
async def upgrade_plan_fail(token: Annotated[str, Depends(verify_token)]):
    return {"message": "Fail to upgrade the plan."}