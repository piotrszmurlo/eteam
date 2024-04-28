from sqlalchemy import (
    create_engine,
    Enum,
    Float,
    Column,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///payment/payment.db")


class PaymentTable(Base):
    __tablename__ = "payments"

    payment_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum("pending", "completed", "failed"), nullable=False)


Base.metadata.create_all(engine)
