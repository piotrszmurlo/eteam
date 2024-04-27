from fastapi import FastAPI, Depends
from typing import Annotated
from common.dependencies import verify_token
from backend.payment.repository import PaymentRepository

payment_app = FastAPI()


@payment_app.post("/create_payment")
async def create_payment(token: Annotated[str, Depends(verify_token)]):
    payment_repo = PaymentRepository()
    return {"message": "hello payment"}
