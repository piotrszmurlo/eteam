import uuid

from typing import Annotated
from venv import logger
from fastapi import FastAPI, Depends, HTTPException
import requests
from common.dependencies import verify_token
from storage.models import (
    UserIdResponse,
    UserModel,
    FileModel,
    FileIdResponse,
    FileInsertModel,
    FileRenameModel,
    FileDeleteModel,
    UpgradePlan,
)
from storage.repository import StorageRepository
from storage.exceptions import (
    UserAlreadyExists,
    UserDoesNotExist,
    FileDoesNotExist,
    StorageLimitExceeded,
)

storage_app = FastAPI()

storage_plans = [
    ["basic", 10, 0],
    ["silver", 50, 50],
    ["gold", 100, 100],
    ["unlimited", float("inf"), 200],
]


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
        raise HTTPException(
            status_code=400, detail=f"User {existing_user_name} already exists!"
        )
    return UserIdResponse(user_id=user_id)


@storage_app.get("/user")
async def get_user(token: Annotated[str, Depends(verify_token)]) -> UserModel:
    storage_repo = StorageRepository()
    user_id = token["sub"]
    # user_id += "1"
    try:
        user = storage_repo.get_user(user_id=user_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    return user


@storage_app.post("/files")
async def add_file(
    file_input: FileInsertModel, token: Annotated[str, Depends(verify_token)]
) -> FileIdResponse:
    storage_repo = StorageRepository()
    file = FileModel(
        user_id=token["sub"],
        file_name=file_input.file_name,
        file_size=file_input.file_size,
    )
    try:
        file_id = storage_repo.insert_file(file)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    except StorageLimitExceeded as e:
        detail_message = f"Storage limit exceded. Currently your plan is {storage_plans[e.current_plan_level][0]}. You lack {e.required_space} Mb."
        upgrade_details = UpgradePlan(
            upgrade_plan_level=e.current_plan_level + 1,
            cost=storage_plans[e.current_plan_level + 1][2],
        )
        print(upgrade_details)
        # TODO: te dane przekazać do NOTIFICATION
        # requests.post
        raise HTTPException(status_code=413, detail=detail_message)
    return FileIdResponse(file_id=file_id)


@storage_app.get("/files")
async def get_files_for_user(
    token: Annotated[str, Depends(verify_token)]
) -> list[FileModel]:
    storage_repo = StorageRepository()
    user_id = token["sub"]
    # user_id += "1"
    try:
        files = storage_repo.get_files(user_id=user_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    return files


@storage_app.patch("/files")
async def rename_file(
    file_id: uuid.UUID,
    file_rename: FileRenameModel,
    token: Annotated[str, Depends(verify_token)],
) -> FileIdResponse:
    storage_repo = StorageRepository()
    try:
        updated_file_id = storage_repo.rename_file(
            file_id=file_id, new_file=file_rename
        )
    except FileDoesNotExist:
        raise HTTPException(status_code=400, detail="File does not exist!")
    return FileIdResponse(file_id=updated_file_id)


@storage_app.delete("/files")
async def delete_file(
    file_delete: FileDeleteModel, token: Annotated[str, Depends(verify_token)]
) -> FileIdResponse:
    storage_repo = StorageRepository()
    try:
        deleted_file_id = storage_repo.delete_file(file_id=file_delete.file_id)
    except FileDoesNotExist:
        raise HTTPException(status_code=400, detail="File does not exist!")
    return FileIdResponse(file_id=deleted_file_id)


@storage_app.patch("/upgrade_plan")
async def upgrade_plan(
    upgrade_details: UpgradePlan,
    token: Annotated[str, Depends(verify_token)],
):
    user_id = token["sub"]
    storage_repo = StorageRepository()
    try:
        logger.debug(upgrade_details)
        logger.debug(type(upgrade_details.upgrade_plan_level))
        storage_repo.update_plan(
            user_id=user_id, plan_level=upgrade_details.upgrade_plan_level
        )
        return {"Plan updated"}

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
