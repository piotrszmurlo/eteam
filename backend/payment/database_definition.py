from sqlalchemy import create_engine, MetaData, Table, Column, String, ForeignKey, Enum, Float

engine = create_engine("sqlite:///payment/payment.db")

metadata_obj = MetaData()

PaymentTable = Table(
    "payments",
    metadata_obj,
    Column("payment_id", String(), primary_key=True),
    Column("user_id", String(128), nullable=False),
    Column("amount", Float(), nullable=False),
    Column("status", Enum("pending", "completed", "failed"), nullable=False),
)

metadata_obj.create_all(engine)
