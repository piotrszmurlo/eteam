from sqlalchemy import create_engine, MetaData, Table, Column, String

engine = create_engine("sqlite:///notification/notification.db")

metadata_obj = MetaData()

UserTable = Table(
    "users",
    metadata_obj,
    Column("user_id", String(), primary_key=True),
    Column("user_name", String(16), nullable=False),
    Column("user_email", String(), nullable=False),
)

metadata_obj.create_all(engine)
