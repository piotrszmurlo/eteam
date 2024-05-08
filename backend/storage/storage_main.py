import uuid
import asyncio
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
import requests
from common.dependencies import verify_token
from storage.models import UserIdResponse, UserModel, FileModel, FileIdResponse, FileInsertModel, FileRenameModel, FileDeleteModel, UpgradePlan, UpgradePlanSuccess
from storage.repository import StorageRepository
from storage.exceptions import UserAlreadyExists, UserDoesNotExist, FileDoesNotExist, StorageLimitExceeded, CannotGetPlan, CannotUpgradePlan
from common.models import UrlResponseModel

storage_app = FastAPI()


@storage_app.get("/hello")
async def root():
    return {"message": "hello storage"}


@storage_app.post("/user")
async def add_user(token: Annotated[str, Depends(verify_token)]) -> UserIdResponse:
    storage_repo = StorageRepository()
    user = UserModel(user_id=token["sub"], user_name=token["given_name"])
    try:
        user_id = storage_repo.insert_user(user)
    except UserAlreadyExists:
        existing_user_name = token["given_name"]
        raise HTTPException(status_code=400, detail=f"User {existing_user_name} already exists!")
    return UserIdResponse(user_id=user_id)


@storage_app.get("/user")
async def get_user(token: Annotated[str, Depends(verify_token)]) -> UserModel:
    storage_repo = StorageRepository()
    user_id=token["sub"]
    try:
        user = storage_repo.get_user(user_id=user_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    return user


@storage_app.post("/files")
async def add_file(file_input: FileInsertModel, token: Annotated[str, Depends(verify_token)]) -> FileIdResponse:
    storage_repo = StorageRepository()
    file = FileModel(user_id=token["sub"], file_name=file_input.file_name, file_size=file_input.file_size)
    try:
        file_id = storage_repo.insert_file(file)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    except StorageLimitExceeded as e:
        upgrade_plan_name = storage_repo.get_required_plan(e.new_total_size)
        upgrade_details = UpgradePlan(current_plan_name=e.current_plan_name, upgrade_plan_name=upgrade_plan_name)
        detail_message = (
            f"Storage limit exceded. Currently your plan is {e.current_plan_name}. You lack {e.required_space} Mb."
        )
        detail_data = UrlResponseModel(url='http://localhost:8000/notification/upgrade_plan', data=upgrade_details.model_dump())
        raise HTTPException(status_code=413, detail={"message": detail_message, "data": detail_data.model_dump()})
    except CannotGetPlan:
        raise HTTPException(status_code=400, detail="Cannot get user's current plan!")
    return FileIdResponse(file_id=file_id)


@storage_app.get("/files")
async def get_files_for_user(token: Annotated[str, Depends(verify_token)]) -> list[FileModel]:
    storage_repo = StorageRepository()
    user_id=token["sub"]
    # user_id += "1"
    try:
        files = storage_repo.get_files(user_id=user_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    return files


@storage_app.patch("/files")
async def rename_file(file_id: uuid.UUID, file_rename: FileRenameModel, token: Annotated[str, Depends(verify_token)]) -> FileIdResponse:
    storage_repo = StorageRepository()
    try:
        updated_file_id = storage_repo.rename_file(file_id=file_id, new_file=file_rename)
    except FileDoesNotExist:
        raise HTTPException(status_code=400, detail="File does not exist!")
    return FileIdResponse(file_id=updated_file_id)


@storage_app.delete("/files")
async def delete_file(file_delete: FileDeleteModel, token: Annotated[str, Depends(verify_token)]) -> FileIdResponse:
    storage_repo = StorageRepository()
    try:
        deleted_file_id = storage_repo.delete_file(file_id=file_delete.file_id)
    except FileDoesNotExist:
        raise HTTPException(status_code=400, detail="File does not exist!")
    return FileIdResponse(file_id=deleted_file_id)


@storage_app.patch("/upgrade_plan")
async def upgrade_plan(data: UpgradePlanSuccess, token: Annotated[str, Depends(verify_token)]):
    storage_repo = StorageRepository()
    user_id = token["sub"]
    try:
        storage_repo.upgrade_plan(user_id=user_id, upgrade_plan_name=data.upgrade_plan_name)
    except CannotGetPlan:
        raise HTTPException(status_code=400, detail="Cannot access PlansTable!")
    except CannotUpgradePlan:
        raise HTTPException(status_code=400, detail="Cannot upgrade user's plan!")
    return {"message": f"Plan of user {user_id} was upgraded to {data.upgrade_plan_name} in storage DB."}