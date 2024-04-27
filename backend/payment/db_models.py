from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Time,
    Boolean,
    Column,
    Integer,
    Enum,
    String,
    Float,
    Date,
    ForeignKey,
)

Base = declarative_base()


class Payment(Base):
    __tablename__ = "payments"

    # Define columns
    payment_id = Column(String, unique=True, nullable=False)
    user_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum("pending", "completed", "failed"), nullable=False)
