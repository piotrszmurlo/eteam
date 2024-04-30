from certifi import where
from sqlalchemy import create_engine, insert, select, update
from payment.models import PaymentModel
from payment.database_definition import PaymentTable


class PaymentRepository:
    engine = create_engine("sqlite:///payment/payment.db")

    def __init__(self) -> None:
        self._connection = self.engine.connect()

    def insert_payment(self, payment: PaymentModel):
        statement = insert(PaymentTable).values(payment.model_dump())
        try:
            self._connection.execute(statement)
            self._connection.commit()
        except:
            pass

    def get_payments(self, user_id: str):
        statement = select(PaymentTable).where(PaymentTable.c.user_id == user_id)
        try:
            payments = self._connection.execute(statement).fetchall()
            return payments
        except:
            pass

    def update_payment_status(self, stripe_id: str, new_status: str):
        statement = (
            update(PaymentTable)
            .where(PaymentTable.c.stripe_id == stripe_id)
            .values(status=new_status)
        )
        try:
            self._connection.execute(statement)
        except:
            pass

    def delete_payment(self):
        pass
