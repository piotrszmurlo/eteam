import uuid
from pydantic import Field
from enum import Enum
from common.base_model import BaseModel


class PlanEnum(str, Enum):
    basic = "basic"
    silver = "silver"
    gold = "gold"
    unlimited = "unlimited"

class UserModel(BaseModel):
    user_id: str                # uuid nie działa, bo user_id=token["sub"] jest stringiem
    user_name: str
    user_plan: int | None = 0

class FileModel(BaseModel):
    file_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    file_name: str
    file_size: float

class FileInsertModel(BaseModel):
    file_name: str
    file_size: float

class UserIdResponse(BaseModel):
    user_id: str

class FileIdResponse(BaseModel):
    file_id: uuid.UUID

class FileRenameModel(BaseModel):
    file_name: str | None = None

class FileDeleteModel(BaseModel):
    file_id: uuid.UUID

class UpgradePlan(BaseModel):
    current_plan_name: str
    upgrade_plan_name: str

class UpgradePlanSuccess(BaseModel):
    upgrade_plan_name: str