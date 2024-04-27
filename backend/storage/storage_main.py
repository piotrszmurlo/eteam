import uuid

from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from common.dependencies import verify_token
from storage.models import UserIdResponse, UserModel, FileModel, FileIdResponse, FileInsertModel, FileRenameModel, FileDeleteModel
from storage.repository import StorageRepository


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
    except:
        existing_user_name = token["given_name"]
        raise HTTPException(status_code=400, detail=f"User {existing_user_name} already exists!")
    return UserIdResponse(user_id=user_id)


@storage_app.get("/user")
async def get_user(token: Annotated[str, Depends(verify_token)]) -> UserModel:
    storage_repo = StorageRepository()
    user_id=token["sub"]
    # user_id += "1"
    try:
        user = storage_repo.get_user(user_id=user_id)
    except:
        raise HTTPException(status_code=400, detail=f"User does not exist!")
    return user


@storage_app.post("/files")
async def add_file(file_input: FileInsertModel, token: Annotated[str, Depends(verify_token)]) -> FileIdResponse:
    storage_repo = StorageRepository()
    file = FileModel(user_id=token["sub"], file_name=file_input.file_name)
    try:
        file_id = storage_repo.insert_file(file)
    except:
        file_name = file_input.file_name
        raise HTTPException(status_code=400, detail=f"File {file_name} already exists!")
    return FileIdResponse(file_id=file_id)


@storage_app.get("/files")
async def get_files_for_user(token: Annotated[str, Depends(verify_token)]) -> list[FileModel]:
    storage_repo = StorageRepository()
    user_id=token["sub"]
    # user_id += "1"
    try:
        files = storage_repo.get_files(user_id=user_id)
    except:
        raise HTTPException(status_code=400, detail=f"User does not exist!")
    return files


@storage_app.patch("/files")
async def rename_file(file_id: uuid.UUID, file_rename: FileRenameModel, token: Annotated[str, Depends(verify_token)]) -> FileIdResponse:
    storage_repo = StorageRepository()
    try:
        updated_file_id = storage_repo.rename_file(file_id=file_id, new_file=file_rename)
    except:
        raise HTTPException(status_code=400, detail=f"File does not exists!")
    return FileIdResponse(file_id=updated_file_id)


@storage_app.delete("/files")
async def delete_file(file_delete: FileDeleteModel, token: Annotated[str, Depends(verify_token)]) -> FileIdResponse:
    storage_repo = StorageRepository()
    try:
        deleted_file_id = storage_repo.delete_file(file_id=file_delete.file_id)
    except:
        raise HTTPException(status_code=400, detail=f"File does not exists!")
    return FileIdResponse(file_id=deleted_file_id)