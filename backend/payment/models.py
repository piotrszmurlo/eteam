from sqlalchemy import Enum, Field
import uuid
from common.base_model import BaseModel


class StatusEnum(str, Enum):
    pending = "pending"
    failed = "failed"
    completed = "completed"


class PaymentModel(BaseModel):
    payment_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    amount: float
    status: StatusEnum
