from pydantic import Field
from enum import Enum
import uuid
from common.base_model import BaseModel

class StatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class PaymentModel(BaseModel):
    payment_id: str             # zmienione bo: (sqlite3.ProgrammingError) Error binding parameter 1: type 'UUID' is not supported
    user_id: str
    amount: float
    status: StatusEnum
