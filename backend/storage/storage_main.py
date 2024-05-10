import uuid
import sys
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
import requests
from starlette.middleware.cors import CORSMiddleware

from authentication.authentication_main import origins
from common.dependencies import verify_token
from storage.models import UserIdResponse, UserModel, FileModel, FileIdModel, FileInsertModel, FileRenameModel, UpgradePlan
from storage.repository import StorageRepository
from storage.file_manager import FileManager
from storage.exceptions import UserAlreadyExists, UserDoesNotExist, FileDoesNotExist, StorageLimitExceeded, CannotGetPlan, CannotUpgradePlan, FileSaveError
from common.models import UrlResponseModel, UpgradePlanArgs

storage_app = FastAPI()

storage_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
async def add_file(file_input: UploadFile, token: Annotated[str, Depends(verify_token)]) -> FileIdModel:
    storage_repo = StorageRepository()
    file_manager = FileManager(user_id=token["sub"])
    contents = await file_input.read()
    contents_mb_size = sys.getsizeof(contents)/1024 ** 2
    file = FileModel(
                    user_id=token["sub"],
                    file_name=file_input.filename,
                    file_size=contents_mb_size)
    limit_exceeded = False
    try:
        file_id = storage_repo.insert_file(file)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    except StorageLimitExceeded as e:
        limit_exceeded = True
        requested_total_storage = e.new_total_size
        current_plan_name = e.current_plan_name
        required_space = e.required_space
    except FileSaveError:
        raise HTTPException(status_code=500, detail="An unexpected error ocurred when trying to save the file")

    if not limit_exceeded:
        file_manager.insert_file(file_id, contents)
        return FileIdModel(file_id=file_id)

    try:
        upgrade_plan_name = storage_repo.get_required_plan(requested_total_storage)
    except CannotGetPlan:
        raise HTTPException(status_code=500, detail="Cannot get user's current plan!")

    upgrade_details = UpgradePlan(current_plan_name=current_plan_name, upgrade_plan_name=upgrade_plan_name)
    detail_message = (
        f"Storage limit exceded. Currently your plan is {current_plan_name}. You lack {required_space} Mb."
    )
    detail_data = UrlResponseModel(url='http://localhost:8000/notification/upgrade_plan', data=upgrade_details.model_dump())
    raise HTTPException(status_code=413, detail={"message": detail_message, "data": detail_data.model_dump()})


@storage_app.get("/files")
async def get_files_for_user(info: Annotated[str, Depends(verify_token)]) -> list[FileModel]:
    storage_repo = StorageRepository()
    user_id = info['sub']
    try:
        files = storage_repo.get_files(user_id=user_id)
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    return files

@storage_app.get("/get_file")
async def get_file_by_id(file_id: FileIdModel, token: Annotated[str, Depends(verify_token)]) -> FileResponse:
    storage_repo = StorageRepository()
    user_id = token["sub"]
    file_manager = FileManager(user_id)
    try:
        file = storage_repo.get_file_by_id(user_id=token['sub'], file_id=str(file_id.file_id))
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail="User does not exist!")
    except FileDoesNotExist:
        raise HTTPException(status_code=400, detail="File does not exist!")
    filename = file.file_name
    filepath = file_manager.get_path_to_file(file_id=file.file_id)
    return FileResponse(filename=filename, path=filepath)


@storage_app.patch("/files")
async def rename_file(file_id: uuid.UUID, file_rename: FileRenameModel, token: Annotated[str, Depends(verify_token)]) -> FileIdModel:
    storage_repo = StorageRepository()
    try:
        updated_file_id = storage_repo.rename_file(file_id=file_id, new_file=file_rename)
    except FileDoesNotExist:
        raise HTTPException(status_code=400, detail="File does not exist!")
    return FileIdModel(file_id=updated_file_id)


@storage_app.delete("/files")
async def delete_file(file_id: uuid.UUID, token: Annotated[str, Depends(verify_token)]) -> FileIdModel:
    storage_repo = StorageRepository()
    try:
        deleted_file_id = storage_repo.delete_file(file_id=file_id)
    except FileDoesNotExist:
        raise HTTPException(status_code=400, detail="File does not exist!")
    return FileIdModel(file_id=deleted_file_id)


@storage_app.patch("/upgrade_plan")
async def upgrade_plan(data: UpgradePlanArgs, token: Annotated[str, Depends(verify_token)]):
    storage_repo = StorageRepository()
    user_id = token["sub"]
    try:
        storage_repo.upgrade_plan(user_id=user_id, upgrade_plan_name=data.upgrade_plan_name)
    except CannotGetPlan:
        raise HTTPException(status_code=400, detail="Cannot access PlanTable!")
    except CannotUpgradePlan:
        raise HTTPException(status_code=400, detail="Cannot upgrade user's plan!")
    return {"message": f"Plan of user {user_id} was upgraded to {data.upgrade_plan_name} in storage DB."}