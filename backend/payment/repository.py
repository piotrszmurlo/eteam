from sqlalchemy.orm import Session


class PaymentRepository:
    def __init__(self, session: Session) -> None:
        self.sess = session

    def insert_payment(self):
        pass

    def get_payments(self, user_id: str):
        pass

    def update_payment(self):
        pass

    def delete_payment(self):
        pass
