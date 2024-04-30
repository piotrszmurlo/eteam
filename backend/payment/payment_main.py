import uuid
from fastapi import FastAPI, Depends, HTTPException, Request, Header
from typing import Annotated
from loguru import logger
from common.dependencies import verify_token
from payment.repository import PaymentRepository
from payment.models import PaymentModel
import stripe

payment_app = FastAPI()

# test key, doesnt need to be hidden
stripe.api_key = "sk_test_51PATYu089JUuVWC5gd49xLoAkxyGGVYgPevTFjOYpRCaTodm7Fr12sfLvpQXHWzkxcxHvjB8fsRa0UAy7jsgJ9BV00AFn9GUfL"
endpoint_secret = (
    "whsec_aebc8b1d7e5afc144f59f329d70ea2388058cdf6482cec9a9c69db9dcffc98ac"
)
# TODO separate files and logic for products and prices
product_name = "Storage limit"
try:
    storage_product = stripe.Product.create(name=product_name, id="storage_1")
except stripe.error.InvalidRequestError as e:
    logger.error(e)
    products = stripe.Product.list(limit=1)
    storage_product = next(
        (prod for prod in products.data if prod.name == product_name), None
    )


async def get_body(request: Request) -> bytes:
    return await request.body()


@payment_app.post("/create_payment")
async def create_payment(token: Annotated[str, Depends(verify_token)], amount: float):
    try:

        price = stripe.Price.create(
            unit_amount=100000,
            currency="usd",
            product=storage_product,
        )
        payment_repo = PaymentRepository()
        payment = PaymentModel(
            payment_id=uuid.uuid4(),
            stripe_id=None,
            user_id=token["sub"],
            amount=amount,
            status="pending",
        )
        payment_repo.insert_payment(payment)

        # TODO in future adjust payment links
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
            payment_method_types=["card"],
        )
        return {"payment link": payment_link.url}

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=422, detail="could not craete payment")


@payment_app.post("/webhook")
def stripe_webhook(
    stripe_signature: Annotated[str, Header(alias="stripe-signature")],
    body: bytes = Depends(get_body),
):
    try:
        payment_repo = PaymentRepository()
        event = stripe.Webhook.construct_event(body, stripe_signature, endpoint_secret)
        # TODO handle other events
        if event.type == "payment_intent.created":
            logger.debug(event)
            # payment_repo.update_payment_status(payment_id=)
        elif event.type == "payment_intent.succeeded":
            logger.debug(event)
        elif event.type == "payment_intent.canceled":
            pass
            # payment = PaymentModel(user_id=token["sub"], amount=amount, status="pending")
            # payment_repo.insert_payment(payment)
        else:
            logger.debug(event.type)
    except ValueError as e:
        logger.error(e)
        return HTTPException(status=400)
    except Exception as e:
        logger.error(e)
