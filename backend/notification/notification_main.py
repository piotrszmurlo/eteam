from typing import Annotated
import requests
from fastapi import FastAPI, Depends, HTTPException
from common.dependencies import verify_token
from notification.models import UserIdResponse, UserModel, FileModel, UserEmailInput, UpgradePlan, SharingFile
from notification.repository import NotificationRepository
from notification.exceptions import UserAlreadyExists, UserDoesNotExist, FileAlreadyExists, FileDoesNotExist
from common.models import UrlResponseModel, UpgradePlanArgs


notification_app = FastAPI()


@notification_app.get("/hello")
async def root() -> dict[str, str]:
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
        user = notification_repo.get_user(user_id=user_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    return user


@notification_app.post("/file")
async def add_file(file: FileModel, token: Annotated[str, Depends(verify_token)]) -> str:
    notification_repo = NotificationRepository()
    try:
        file_id = notification_repo.add_file(file)
    except FileAlreadyExists:
        raise HTTPException(status_code=400, detail=f"File {file.file_id} already exists!")
    return file_id


@notification_app.get("/file")
async def get_file(file_id: str, token: Annotated[str, Depends(verify_token)]) -> FileModel:
    notification_repo = NotificationRepository()
    try:
        file = notification_repo.get_file(file_id=file_id)
    except FileDoesNotExist:
        raise HTTPException(status_code=400, detail="File does not exist!")
    return file


@notification_app.post("/upgrade_plan")
async def upgrade_plan(upgrade_details: UpgradePlan, token: Annotated[str, Depends(verify_token)]) -> UrlResponseModel:

    print(f"NOTIFICATION: Your current plan is {upgrade_details.current_plan_name} and you need to upgrade to {upgrade_details.upgrade_plan_name}")

    create_payment_details = UpgradePlanArgs(upgrade_plan_name=upgrade_details.upgrade_plan_name)

    url_response = UrlResponseModel(url='http://localhost:8000/payment/create_payment', data=create_payment_details)

    print(f"URL do paymentu: {url_response}")

    return url_response


@notification_app.get("/upgrade_plan_success")
async def upgrade_plan_success(data: UpgradePlanArgs, token: Annotated[str, Depends(verify_token)]) -> dict[str, str]:
    return {"message": f"Your plan has been upgraded to{data.upgrade_plan_name}"}


@notification_app.get("/upgrade_plan_fail")
async def upgrade_plan_fail(token: Annotated[str, Depends(verify_token)]) -> dict[str, str]:
    return {"message": "Fail to upgrade the plan."}


@notification_app.post("/sharing_notification")
async def add_sharing_notification(sharing_data: SharingFile, token: Annotated[str, Depends(verify_token)]) -> str:
    notification_repo = NotificationRepository()
    try:
        file_id = notification_repo.add_notification(sharing_data)
    except Exception:
        raise HTTPException(status_code=400, detail="Cannot add sharing notification.")
    return file_id


@notification_app.patch("/sharing_notification")
async def update_sharing_notification_status(file_id: str, token: Annotated[str, Depends(verify_token)]) -> str:
    notification_repo = NotificationRepository()
    try:
        file_id = notification_repo.update_notification_status(file_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Cannot update notification status.")
    return {"file_id": file_id, "status": "updated"}