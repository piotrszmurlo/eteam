
from common.base_model import BaseModel


class UserModel(BaseModel):
    user_id: str
    user_name: str
    user_email: str

class UserIdResponse(BaseModel):
    user_id: str

class UserEmailInput(BaseModel):
    user_email: str

class UpgradePlan(BaseModel):
    upgrade_plan_level: int
    cost: int