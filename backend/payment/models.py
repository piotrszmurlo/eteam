from pydantic import Field
from enum import Enum
import uuid
from common.base_model import BaseModel


class StatusEnum(str, Enum):
    pending = "pending"
    created = "created"
    failed = "failed"
    completed = "completed"


class PaymentModel(BaseModel):
    payment_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    stripe_id: str | None
    user_id: str
    amount: float
    status: StatusEnum
