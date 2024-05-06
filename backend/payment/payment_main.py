import uuid
from fastapi import FastAPI, Depends, HTTPException, Request, Header
from typing import Annotated
from loguru import logger
from common.dependencies import verify_token
from payment.repository import PaymentRepository
from payment.models import PaymentModel
from payment.exceptions import PaymentDataBaseError, StripePaymentError
import stripe
from starlette.responses import RedirectResponse
import datetime

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


@payment_app.get("/payment_success")
async def payment_success(user_id: str):
    payment_repo = PaymentRepository()

    user_payments = payment_repo.get_payments(user_id=user_id, status="pending")
    stripe_events = stripe.Event.list(limit=10, type="checkout.session.completed", created={"gt": datetime.datetime.now(tz=None)-datetime.timedelta(seconds=15)})

    for event in stripe_events:
        checkout_id = event['data']['object'].get('id')
        if checkout_id in [u.payment_id for u in user_payments]:
            payment_repo.update_payment_status(payment_id=checkout_id, new_status="completed")
        
    # TODO: UDERZYĆ DO NOTIFICATION
    # TODO: UDERZYĆ DO STORAGE --> update plan
    return{"Success payment - payment id": checkout_id}

@payment_app.get("/payment_cancel")
async def payment_cancel():
    # TODO: UDERZYĆ DO NOTIFICATION
    return{"Payment cancelled"}


@payment_app.post("/create_payment")
async def create_payment(amount: int, token: Annotated[str, Depends(verify_token)]):
    try:
        price = stripe.Price.create(
            unit_amount=100 * amount,
            currency="usd",
            product=storage_product,
        )
        # # TODO in future adjust payment links
        # stripe_payment_link = stripe.PaymentLink.create(
        #     line_items=[{"price": price.id, "quantity": 1}],
        #     payment_method_types=["card"],
        # )
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': f'{price.id}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'http://localhost:8000/payment/payment_success?user_id={token["sub"]}',
            cancel_url='http://localhost:8000/payment/payment_cancel',
        )
    except StripePaymentError:
        raise HTTPException(status_code=500, detail="Could not create new payment in Stripe.")

    payment_repo = PaymentRepository()
    payment = PaymentModel(
        payment_id=checkout_session.id,
        user_id=token["sub"],
        amount=amount,
        status="pending",
        )
    try:
        payment_repo.insert_payment(payment)
    except PaymentDataBaseError:
        raise HTTPException(status_code=400, detail="Could not register a new payment in database.")
    print("Link to payment:")
    print(checkout_session.url)
    return checkout_session.url
    # return RedirectResponse(url=checkout_session.url)


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
