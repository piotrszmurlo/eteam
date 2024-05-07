from pydantic import Field
from enum import Enum
import uuid
from common.base_model import BaseModel
from common.models import UrlResponseModel

class StatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class PaymentModel(BaseModel):
    payment_id: str             # zmienione bo: (sqlite3.ProgrammingError) Error binding parameter 1: type 'UUID' is not supported
    user_id: str
    status: StatusEnum

class CreatePaymentModel(BaseModel):
    upgrade_plan_name: str

class PaymentSuccessModel(BaseModel):
    notification_url: UrlResponseModel
    storage_url: UrlResponseModel