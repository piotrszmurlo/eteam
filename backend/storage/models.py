import uuid

from pydantic import Field

from common.base_model import BaseModel


class UserModel(BaseModel):
    user_id: str                # uuid nie działa, bo user_id=token["sub"] jest stringiem
    user_name: str



class FileModel(BaseModel):
    file_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    file_name: str


class FileInsertModel(BaseModel):
    file_name: str


class UserIdResponse(BaseModel):
    user_id: str


class FileIdResponse(BaseModel):
    file_id: uuid.UUID


class FileRenameModel(BaseModel):
    file_name: str | None = None


class FileDeleteModel(BaseModel):
    file_id: uuid.UUID
