from fastapi import FastAPI, Depends
from typing import Annotated
from loguru import logger
from common.dependencies import verify_token
from payment.repository import PaymentRepository
from payment.models import PaymentModel

payment_app = FastAPI()


@payment_app.post("/create_payment")
async def create_payment(token: Annotated[str, Depends(verify_token)], amount: float):
    try:
        payment_repo = PaymentRepository()
        payment = PaymentModel(user_id=token["sub"], amount=amount, status="pending")
        payment_repo.insert_payment(payment)
    except Exception as e:
        logger.error(e)

    return {"payment link": "https://buy.stripe.com/test_5kA8xr8DS4eNaR2fYY"}
