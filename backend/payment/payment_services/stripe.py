import stripe

# test api key
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


def create_payment(amount, currency, source):
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=source,
            description="Charge for a service or product",
        )
        return charge
    except stripe.error.StripeError as e:
        return str(e)
