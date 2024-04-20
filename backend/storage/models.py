import uuid

from pydantic import Field

from common.base_model import BaseModel


class UserModel(BaseModel):
    user_id: str
    user_name: str

    class Config:
        from_attributes = True


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
